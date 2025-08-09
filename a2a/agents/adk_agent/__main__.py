import logging
import os

import click
import httpx

from a2a.server.apps import A2AStarletteApplication, A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, InMemoryPushNotifier
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent import GoogleADKAgent
from agent_executor import GoogleADKAgentExecutor
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', default=10001)
def main(host, port):
    try:
        # Check for API key only if Vertex AI is not configured
        if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') == 'TRUE':
            if not os.getenv('GOOGLE_API_KEY'):
                raise MissingAPIKeyError(
                    'GOOGLE_API_KEY environment variable not set and GOOGLE_GENAI_USE_VERTEXAI is not TRUE.'
                )

        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id='asisstent_adk',
            name='Spesialis Agent AI Framework ADK',
            description='Membantu menjelaskan konsep, arsitektur, dan cara kerja Google ADK (Agent Development Kit) untuk membuat agent AI.',
            tags=['google', 'adk', 'agent ai', 'framework', 'library', 'google adk'],
            examples=[
                'apa itu google adk?',
                'jenis-jenis type agent di google adk',
                'apa saja built-in-tools tools di google adk',
            ],
        )
        agent_card = AgentCard(
            name='Google ADK Asisstent Agent',
            description='Agent ini memiliki pengetahuan dalam tentang library Google ADK (Agent Development Kit) untuk membuat agent AI.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            defaultInputModes=GoogleADKAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=GoogleADKAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )
        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=GoogleADKAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client)
        )
        
        #server = A2AStarletteApplication(
        #    agent_card=agent_card, http_handler=request_handler
        #)

        fastapi_server = A2AFastAPIApplication(
            agent_card=agent_card,
            http_handler=request_handler,
        )

        import uvicorn

        #uvicorn.run(server.build(), host=host, port=port)
        uvicorn.run(fastapi_server.build(), host=host, port=port)
    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        exit(1)


if __name__ == '__main__':
    main()