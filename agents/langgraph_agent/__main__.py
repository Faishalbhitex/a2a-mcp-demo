import logging
import os
import sys

import click
import httpx
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from dotenv import load_dotenv

from agent import LangGraphAgent
from agent_executor import LangGraphAgentExecutor


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MissingAPIKeyError(Exception):
    "Exception untuk missing API Key"

@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10003)
def main(host, port):
    try:
        gemini = os.getenv("GOOGLE_API_KEY")
        brave_search = os.getenv("BRAVE_SEARCH_API_KEY")

        if not gemini and not brave_search:
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY dan BRAVE_SEARCH_API_KEY enviroment belum di setup salahsatunya."
            )
        
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id='asisstent_langgraph',
            name='Spesialis Agent AI Framework LangChain, LangGraph, LangSmith, dan LangFlow',
            description=(
                'Menjelaskan apa itu LangChain, LangGraph, LangSmith, dan LangFlow'
                'Memandu cara menggunakan langchain, langgraph, langsmith dan langflow dalam pembuatan agent ai.'
            ),
            tags=["agent ai", "chain", "graph", "smith", "flow", "framework", "library", "workflow"],
            examples=[
                "Apa itu langchain?",
                "Apa bedanya langchain, langgraph, langsmith dan langflow?",
            ],
        )
        agent_card = AgentCard(
            name='LangGraph Asisstent Agent',
            description='Membantu untuk bikin agent ai dengan langchain dan komponent langchain lainnya.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=LangGraphAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=LangGraphAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=LangGraphAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler,
        )

        uvicorn.run(server.build(), host=host, port=port)
    
    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Terjadi kesalahan saat memulai server: {e}.')
        sys.exit(1)

if __name__ == '__main__':
    main()

