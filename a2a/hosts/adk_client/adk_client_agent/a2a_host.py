import json    
import httpx
import logging
from uuid import uuid4
from a2a.client import A2ACardResolver
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    TextPart,
)
from .agent_server_connection import AgentServerConnections
from google.adk import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class A2AADKAgentClient:

    def __init__(self):
        self.agent_server_connections: dict[str, AgentServerConnections] = {}
        self.agent_cards: dict[str, AgentCard] = {}
        self.agent_names: list[str] = []
    
    async def _init_agent_server(self, agent_urls: str, default_timeout: float = 30.0):
            self.agent_urls = agent_urls
            self.httpx_client = httpx.AsyncClient(timeout=default_timeout)
            for agent_url in self.agent_urls:
               card_esolver = A2ACardResolver(
                    httpx_client=self.httpx_client,
                    base_url=agent_url.rstrip('/'),
               )
               try:
                    card = await card_esolver.get_agent_card()
                    logger.info(f"Success fecth Agent Card from {agent_url}\n")
                    agent_conn = AgentServerConnections(httpx_client=self.httpx_client, card=card)
                    self.agent_server_connections[card.name] = agent_conn
                    self.agent_cards[card.name] = card
                    self.agent_names.append(card.name)
                    logger.info(f"Success Connect to Agent URL: {agent_url}, Agent Server Name: {card.name}\n")
               
               except httpx.ConnectError as e:
                    logger.error(f"Agent Url {agent_url} disscconect or din't exists: {e}")
               except Exception as e:
                    logger.error(e)

    async def close(self):
         await self.httpx_client.aclose()

    @classmethod
    async def create(
         cls,
         agent_urls: list[str]
    ) -> 'A2AClientTools':
         instance = cls()
         await instance._init_agent_server(agent_urls=agent_urls)
         return instance
    

    async def list_server_agents(self):
         "List server agent atau remote agent yang tersedia untuk nama dan deskripsi-nya."
         if self.agent_cards is None:
              return f"Agent Server atau Agent Remote tidak tersedia."
         agent_server_info = []
         for name in self.agent_cards:
              agent_name = self.agent_cards[name].name
              agent_description = self.agent_cards[name].description
              agent_server_info.append(
                   {
                        "name": agent_name,
                        "description": agent_description,
                   },
              )
        
         return agent_server_info
    
    async def send_message(self, agent_name: str, msg: str):
         """
         Mengirimkan pesan atau tugas(task) ke agent server/remote secara streaming(jika support) dan non-streaming.
         
         Args:
               agent_name (str): Nama agent server atau aget remote yang tersedia.
               msg: Pesan yang di kirim ke agent atau Tugas yang di delegasikan.
          
         Return:
          berupa dictonary response status dan text/task
         """
         if agent_name not in self.agent_names:
              return {
                   "status": False,
                   "error": f"Agent Server {agent_name} tidak tersedia."
              }
         #logger.info(f"send_message (agent_name): {agent_name}")
         client = self.agent_server_connections[agent_name]
         #logger.info(f"send_message (client): {client}")

         message: Message = Message(
              role='user',
              parts=[TextPart(text=msg)],
              messageId=str(uuid4()),
              contextId=str(uuid4()),
              taskId=str(uuid4())
         )

         request: MessageSendParams = MessageSendParams(
              message=message,
         )
         response = await client.send_message(request=request)
         #logger.info(f"send_message (response): {response}\n")
         return response
    

    def create_agent(self) -> Agent:
         return Agent(
              model='gemini-2.0-flash-001',
              name='host_agent',
              instruction=self.root_instruction,
              description="agent delegasi tugas antar agent remote atau agent server.",
              tools=[
                   self.list_server_agents,
                   self.send_message,
              ]
         )
    
    def root_instruction(self, context: ReadonlyContext) -> str:
         return f"""
          Kamu adalah host agent atau client agent yang mendelegasi tugas ke agent remote atau agent server.

          anda diberikan tools `list_server_agent` untuk cek agent server atau remote yang tersedia beserta nama dan deskirpsinya kemapuan agent tersebut.
          dan tools `send_message` untuk memberikan tugas atau mengirimkan pesan ke agent server tersebut.

          topik anda kebanyakan akan seputar pembahas bagaimana membuat agent ai untuk kebutuhan automasi.
          """
    
    async def stream(self, agent: Agent, msg: str, session_id: str = None):
          """Kirim Message Agent Host secara streaming"""
          session_service = InMemorySessionService()
          #APP_NAME ="a2a_adk_client"
          USER_ID = str(uuid4())
          SESSION_ID = session_id if session_id else str(uuid4())

          if msg is None:
               raise ValueError("Message cannot be empty.")
          yield {
               "State": "💬 Human Message",
               "Message": msg
          }
          
          runner = Runner(
               app_name=agent.name,
               agent=agent,
               session_service=session_service
          )

          session = await runner.session_service.get_session(
            app_name=agent.name,
            user_id=USER_ID,
            session_id=SESSION_ID,
          )
          content = types.Content(
               role='user', parts=[types.Part.from_text(text=msg)]
          )

          if session is None:
               session = await runner.session_service.create_session(
                    app_name=agent.name,
                    user_id=USER_ID,
                    state={},
                    session_id=SESSION_ID,
               )
          
          async for event in runner.run_async(
               user_id=USER_ID,
               session_id=SESSION_ID,
               new_message=content
          ):
               if event.get_function_calls():
                    for tool_call in event.get_function_calls():
                         tool_name = tool_call.name
                         tool_args = tool_call.args
                         yield {
                              "State": "🛠️ Tool Call",
                              "Tool Name": tool_name,
                              "Tool Args": json.dumps(tool_args, indent=2, ensure_ascii=False)
                         }
               if event.get_function_responses():
                    for tool_response in event.get_function_responses():
                         tool_name = tool_response.name
                         result_dict = tool_response.response
                         yield {
                              "State": "📩 Tool Message",
                              "Tool Message Name": tool_name,
                              "Message": result_dict
                         }
               if event.is_final_response():
                    if event.content and event.content.parts:
                         agent_response = event.content.parts[0].text
                         yield {
                              "State": "🤖 Agent Message",
                              "Message": agent_response
                         }
          
