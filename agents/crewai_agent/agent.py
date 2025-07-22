from collections.abc import AsyncIterable
from typing import Any
from crewai import LLM, Agent, Task, Crew
from crewai_tools import SerperDevTool
from crewai.process import Process
import os
from dotenv import load_dotenv

load_dotenv()


class CrewAIAgent:

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        if os.getenv("GOOGLE_API_KEY"):
            self.model = LLM(
                model="gemini/gemini-2.0-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
            )
        elif os.getenv("OPENAI_API_KEY"):
            self.model = LLM(
                model="gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        
        if not os.getenv('SERPER_API_KEY'):
            raise ValueError("SERPER_API_KEY enviromen tidak di setup.")
        
        self.crewai_assistent_agent = Agent(
            role="Asisstent CrewAI Agent",
            goal=(
                "Memberikan infromasi khusus untuk pembuatan CrewAI Agent."
                "Selalu mencari informasi di sumber dokumentasi 'https://docs.crewai.com/en/introduction' untuk menjawab pertanyaan user untuk bikin agent ai dengan crewai framework."
                "Gunakan selalu tools yang tersedia untuk mendapatkan informasi yang dibutuhkan di bidang CrewAI."
            ),
            backstory=(
                "Kamu adalah asisten AI spesialis CrewAI. Kamu tidak menjawab pertanyaan tentang LangChain, AutoGen, LlamaIndex, atau framework lain.\n"
                "Kamu dilatih untuk menjawab secara profesional hanya dalam domain CrewAI, dan akan sopan menolak jika di luar itu.\n"
                "Kamu juga dilatih untuk hemat dalam menggunakan tool — hanya gunakan jika tidak bisa dijawab langsung oleh kamu sendiri."
            ),
            allow_delegation=False,
            verbose=False,
            tools=[SerperDevTool()],
            llm=self.model,
        )

        self.crewai_assistent_task = Task(
            description=(
                "User memberikan prompt: '{user_prompt}'.\n"
                "Tugas kamu:\n"
                "- Jika user hanya menyapa ('hai', 'halo', 'hai nama saya [nama]), balas ramah beserta namanya jika user include namanya atau jika anda ingat dan arahkan ke topik CrewAI secara perlahan.\n"
                "- Jika user membahas CrewAI (agent/task/crew/proses), jawab secara teknis dan profesional.\n"
                "- Jika user menyebut framework lain seperti LangChain atau LlamaIndex, beri tahu bahwa kamu hanya dapat menjelaskan CrewAI.\n"
                "- Hanya gunakan tool jika benar-benar perlu untuk menjawab hal teknis tentang dokumentasi CrewAI.\n"
                "- Jika bisa dijawab langsung, JANGAN gunakan tool apapun."
            ),

            expected_output="Jawaban berbentuk penjelasan teks (1-3 paragraf) tentang CrewAI framework, komponennya, dan contoh penerapan real-world.",
            agent=self.crewai_assistent_agent,
        )
        
        self.crewai_assistent_crew = Crew(
            agents=[self.crewai_assistent_agent],
            tasks=[self.crewai_assistent_task],
            process=Process.sequential,
            verbose=False,
        )
    
    def invoke(self, query, session_id) -> str:
        inputs = {
            "user_prompt": query,
            "session_id": session_id,
        }
        try:
            response = self.crewai_assistent_crew.kickoff(inputs)
            return str(response)
        except Exception as e:
            return f"❌ Terjadi kesalahan saat menjalankan CrewAI: {str(e)}"

    
    async def stream(self, quer: str) -> AsyncIterable[dict[str, Any]]:
        """Streaming belum support di CrewAI."""
        raise NotImplementedError("Streaming belum support di CrewAI.")