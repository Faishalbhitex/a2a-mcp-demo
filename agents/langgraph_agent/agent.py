import os

from collections.abc import AsyncIterable
from typing import Any, Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_community.tools import BraveSearch
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

memory = MemorySaver()

class ResponseFormat(BaseModel):
    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str

class LangGraphAgent:
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    SYSTEM_INSTRUCTION = """
    Anda adalah seorang ahli spesialis dalam ekosistem LangChain yang mencakup:

    **BIDANG KEAHLIAN:**
    - **LangChain**: Framework untuk membangun aplikasi dengan LLM, chains, agents, memory, callbacks
    - **LangGraph**: Framework untuk membangun stateful, multi-actor applications dengan LLM
    - **LangSmith**: Platform untuk debugging, testing, evaluating, dan monitoring LLM applications
    - **LangFlow**: Visual interface untuk membangun LangChain flows dengan drag-and-drop

    **TUGAS ANDA:**
    1. Analisis apakah pertanyaan berkaitan dengan LangChain ecosystem (LangChain, LangGraph, LangSmith, LangFlow)
    2. Jika YA: Berikan jawaban detail dan akurat dengan melakukan pencarian dokumentasi terbaru jika diperlukan
    3. Jika TIDAK: Jelaskan sopan bahwa Anda spesialis LangChain ecosystem dan arahkan ke sumber yang sesuai
    4. Gunakan tool pencarian untuk mendapatkan informasi terbaru dari dokumentasi resmi
    5. Berikan contoh kode praktis dan implementasi yang relevan
    6. Sertakan best practices dan troubleshooting tips
    7. Jawab dalam bahasa Indonesia dengan jelas dan terstruktur

    **FOKUS UTAMA:**
    - Implementasi praktis dan hands-on examples
    - Integrasi antar komponen LangChain ecosystem  
    - Performance optimization dan debugging
    - Latest features dan updates
    - Common pitfalls dan solutions

    Selalu prioritaskan akurasi informasi dan berikan referensi dokumentasi yang tepat.
    """

    FORMAT_INSTRUCTION = (
        'Set respon status input_required jika user  membutuhkan informasi untuk menyelesaikan atau complete permintaan.'
        'Set respon status error jika terjadi error saat tools tidak bekerja dengan benar.'
        'Set respon status completed jika permintaan sudah selesai.'
    )

    def __init__(self):
        model_source = os.getenv('model_source', 'google')
        if model_source == 'google':
            self.model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
        if not os.getenv('TAVILY_API_KEY'):
            raise ValueError("TAVILY_API_KEY enviroment belum di setup untuk menggunakan tools search brave search.")
        
        tavily_search_tool = TavilySearch(max_result=5, topic="general")
        
        self.tools = [tavily_search_tool]

        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=(self.FORMAT_INSTRUCTION, ResponseFormat),
        )
    
    async def stream(self, query: str, context_id: str) -> AsyncIterable[dict[str, Any]]:
        inputs = {'messages': [('user', query)]}
        config = {'configurable': {'thread_id': context_id}}

        try:
            for item in self.graph.stream(inputs, config, stream_mode='values'):
                message = item['messages'][-1]
                if (
                    isinstance(message, AIMessage)
                    and message.tool_calls
                    and len(message.tool_calls) > 0
                ):
                    yield {
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': 'Mencari informasi terbaru dari dokumentasi LangChain...',
                    }
                elif isinstance(message, ToolMessage):
                    yield {
                        'is_task_complete': False,
                        'require_user_input': False,
                        'content': 'Menganalisis dan menyusun jawaban berdasarkan informasi yang ditemukan...',
                    }

            yield self.get_agent_response(config)
        except Exception as e:
            yield {
                'is_task_complete': False,
                'require_user_input': True,
                'content': f'Terjadi kesalahan saat memproses permintaan: {str(e)}. Silakan coba lagi.',
            }
            

    def get_agent_response(self, config):
        try:
            current_state = self.graph.get_state(config)
            structured_response = current_state.values.get('structured_response')
            if structured_response and isinstance(structured_response, ResponseFormat):
                if structured_response.status == 'input_required':
                    return {
                        'is_task_complete': False,
                        'require_user_input': True,
                        'content': structured_response.message,
                    }
                if structured_response.status == 'error':
                    return {
                        'is_task_complete': False,
                        'require_user_input': True,
                        'content': structured_response.message,
                    }
                if structured_response.status == 'completed':
                    return {
                        'is_task_complete': True,
                        'require_user_input': False,
                        'content': structured_response.message,
                    }
                
            return {
                'is_task_complete': False,
                'require_user_input': True,
                'content': (
                    'Tidak dapat memproses permintaan Anda saat ini. '
                    'Silakan coba lagi atau reformulasi pertanyaan Anda.'
                ),
            }
        
        except Exception as e:
            return {
                'is_task_complete': False,
                'require_user_input': True,
                'content': (
                    f'Terjadi kesalahan saat mengambil response: {str(e)}. '
                    'Silakan coba lagi.'
                ),
            }