import logging
import json

from typing import Any
from uuid import uuid4
import asyncio

import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
    SendStreamingMessageSuccessResponse,
    Task,
    TaskStatus,
    Artifact,
    TaskArtifactUpdateEvent,
    TaskStatusUpdateEvent,
    Part,
    TextPart,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main(use_stream=True) -> None:
    url = 'http://localhost:10001'

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=url,
        )
        _public_card = (
            await resolver.get_agent_card()
        )
        logger.info(_public_card.model_dump_json(indent=2, exclude_none=True))
        agent_card: AgentCard = _public_card
    
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card,
        )
        logger.info(f'\nInsialisasi A2A Client: {client}')

        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {
                        'kind': 'text',
                        'text': 'Hello'
                    },
                ],
                'messageId': str(uuid4()),
            },
        }
        logger.info(f'\nBuat pesan: {json.dumps(send_message_payload, indent=2)}')

        if agent_card.capabilities.streaming == True:
            if use_stream:
                logger.info('Support Streaming.')           
                stream_request = SendStreamingMessageRequest(
                    id=str(uuid4()),
                    params=MessageSendParams(**send_message_payload)
                )
                logger.info(f'Membuat permintaan atau request stream: {stream_request.model_dump_json(indent=2)}')
                #task = None
                final_response = ''
                i = 1
                stream_response = client.send_message_streaming(stream_request)
                async for resp in stream_response:
                    print(f'\n#{30 * '='} STREAM KE-{i} {30 * '='}#\n')
                    logger.info(f'Response stream dari request ke-{i}: {type(resp)}\n')

                    if not resp.root.result:
                        raise ValueError(resp.root.error)
                    
                    event = resp.root.result
                    #logger.info(f'Event ke-{i}: {event}\n')
                    logger.info(f'Event ke-{i} type: {type(event)}\n')

                    if isinstance(event, Task):
                        task_id = event.id
                        task_state = event.status
                        logger.info(f'Task Id: {task_id}\n')
                        if isinstance(task_state, TaskStatus):
                            logger.info(f'Task State: {task_state.state}\n')
                    
                    if isinstance(event, TaskArtifactUpdateEvent):
                        artifact= event.artifact
                        context_id = event.contextId
                        task_id = event.taskId
                        logger.info(f'Context Id: {context_id}\n')
                        if isinstance(artifact, Artifact):
                            logger.info(f'Artfact: {artifact}\n')
                            final_response = artifact.parts[0].root.text
                        logger.info(f'Task id: {task_id}')
                    
                    if isinstance(event, TaskStatusUpdateEvent):
                        context_id = event.contextId
                        task_state = event.status
                        logger.info(f'Context Id: {context_id}\n')
                        if isinstance(task_state, TaskStatus):
                            logger.info(f'Task State: {task_state.state}\n')

                    i += 1

                print(f'\n#{30 * '='} Agent Server Response {30 * '='}#\n')
                print(final_response)
                            
            else:
                logger.info('Non-Streaming.')
                req = SendMessageRequest(
                    id=str(uuid4()),
                    params=MessageSendParams(**send_message_payload)
                )
                logger.info(f'\nMembuat permintaan atau request: {req.model_dump_json(indent=2)}')
                resp = await client.send_message(req)
                print(resp.model_dump_json(indent=2))
        
        else:
            # Default Non-Streaming jika agent card tidak support streaming
            logger.info('Tidak Support Streaming use_stream diInit ke False.')
            use_stream=False
            req = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**send_message_payload)
            )
            logger.info(f'\nMembuat permintaan atau request: {req.model_dump_json(indent=2)}')
            resp = await client.send_message(req)
            print(resp.model_dump_json(indent=2))






if __name__ == '__main__':
    asyncio.run(main())