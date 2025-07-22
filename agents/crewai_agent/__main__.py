import logging
import os

import click

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import CrewAIAgent
from agent_executor import CrewAIAgentExecutor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MissingAPIKeyError(Exception):
    """Exception untuk missing API key."""

@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=10002)
def main(host, port):
    try:
        if not os.getenv('GOOGLE_API_KEY'):
            raise MissingAPIKeyError("GOOGLE_API_KEY atau OPENAI_API_KEY enviroment variabel belum di setup")
        
        capabilities = AgentCapabilities(streaming=False)
        skill =  AgentSkill(
            id='asisstent_crewai',
            name='Spesialis Agent AI Framework CrewAI',
            description=(
                "Memebantu memandu cara membuat agent ai dengan crewai."
                "Memehami konsep-konsep CrewAI secara up-to-date atau informasi terbaru."
                "Menjelaskan konsep crew, flow dan lainnya di crewai langsung dari dokumentasi resminya."
            ),
            tags=[
                "crewai", 'agent ai', "crew", "flow", "framework", "lbrary"
            ],
            examples=[
                "Apa itu crewai?",
                "Apa itu crew dan flow dalam crewai?"
            ],
        )
        agent_host_url = (
            os.getenv('HOST_OVERRIDE') if os.getenv('HOST_OVERRIDE')
            else f'http://{host}:{port}/'
        )
        agent_card = AgentCard(
            name='CrewAI Asisstent Agent',
            description='Agent dengan kemampuan mendalam atau spesialis di bidang library atau framework CrewAI untuk pembuatan agent ai.',
            url=agent_host_url,
            version='1.0.0',
            defaultInputModes=CrewAIAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=CrewAIAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],  
        )

        request_handler = DefaultRequestHandler(
            agent_executor=CrewAIAgentExecutor(),
            task_store=InMemoryTaskStore(),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler,
        )
        import uvicorn

        uvicorn.run(server.build(), host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f"Terjadi kesalahan saat memulai server: {e}.")
        exit(1)


if __name__ == '__main__':
    main()
    