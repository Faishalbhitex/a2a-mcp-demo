from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types
from collections.abc import AsyncIterable
from typing import Any



class GoogleADKAgent:

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = "adk_remote_agent"
        self._runner =Runner(
            app_name=self._agent.name,
            agent=self._agent,
            session_service=InMemorySessionService(),
            artifact_service=InMemoryArtifactService(),
            memory_service=InMemoryMemoryService(),
        )
    
    def _build_agent(self) -> Agent:
        return Agent(
            model="gemini-2.0-flash-001",
            name="adk_assistent_agent",
            description=(
                "Agent adk atau lebih tepatnya Agent Develoment Kit (ADK) adalah agent spesialis di bidang framework agent ai milik Google"
                "Menjelaskan konsep, arsitektur, dan cara kerja Google ADK."
            ),
            instruction="""
            Anda adalah agent spesialis di bidang framework atau libra Google ADK (Agent Development Kit) untuk membuat agent ai tersebut.
            ADK di buat padah tahun 2025 oleh google untuk membuat agent ai ataupun multi agent ai jadi lebih mudah dan cepat produksi.

            Dalam ADK terdapat beberapa komponen penting seperti:
            - Agent
            - Tools
            - Sessions dan Memory
            - Artifacts
            - Callbacks
            - Events
            - Context

            **Anda harus menggunakan tools 'google_search' unntuk mengambil informasi dari dokumentasi Gogle ADK.**

            # **Query wajib anda gunakan dalam searching:**
              ## Agents
                - 'https://google.github.io/adk-docs/agents/' 
                note: anda bisa menambahkan query tambahan setelah slash '/agents/' tersebut seperti '/llm-agents', 'workflow-agents', dan 'custom-agents'.
              ## Tools
                - 'https://google.github.io/adk-docs/tools/'
                note: sama seperti hastag agents anda bisa menemukan informasi tambahan dengan menambahkn setelah slash '/tools/' sperti '/function-tools', '/built-in-tools' dan '/mcp-tools'.
              ## Sessions dan Memory
              ....
            
            Di atas contohnya ang penting anda harus memulai dengan query 'https://google.github.io/adk-docs/' lalu anda bisa tambhakn slash dari komponent penting yang saya sebutkan sebelumnya dengan lowerccase.
            """,
            tools=[google_search],
            generate_content_config=types.GenerateContentConfig(
                temperature=0.2,
            ),
        )
    
    def get_processing_message(self) -> str:
        return (
            "Sedang memproses permintaan Anda. "
            "Mohon tunggu sebentar, saya akan segera memberikan informasi yang Anda butuhkan."
        )
    
    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=query)]
        )

        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
            
        async for event in self._runner.run_async(
        user_id=self._user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                response = ''
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    response = '\n'.join(
                        [p.text for p in event.content.parts if p.text]
                    )
                elif (
                    event.content
                    and event.content.parts
                    and any(
                        [
                            True
                            for p in event.content.parts
                            if p.function_response
                        ]
                    )
                ):
                    response = next(
                        p.function_response.model_dump()
                        for p in event.content.parts
                    )
                yield {
                    'is_task_complete': True,
                    'content': response,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }