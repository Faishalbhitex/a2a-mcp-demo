import logging
import httpx
from uuid import uuid4


from a2a.client import A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
    Task,
    Artifact,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    TaskState,
    SendMessageSuccessResponse,
    SendStreamingMessageSuccessResponse,
)
from a2a.client.errors import A2AClientHTTPError, A2AClientJSONError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentServerConnections:
    
    def __init__(self, httpx_client: httpx.AsyncClient, card: AgentCard):
        self.client = A2AClient(
                    httpx_client=httpx_client,
                    agent_card=card,
        )
        self.agent_card = card
    
    async def send_message(
        self, 
        request: MessageSendParams,
    ) -> SendMessageSuccessResponse | SendStreamingMessageSuccessResponse:
        task_id = None
        context_id = None
        response = ""
        types = ""
        response_type = ""
        if self.agent_card.capabilities.streaming:
            response_type = "Streaming"
            request_stream = SendStreamingMessageRequest(
                id=str(uuid4()),
                params=request,
            )
            stream_response = self.client.send_message_streaming(request_stream)

            async for stream in stream_response:
                event = stream.root.result
                if isinstance(event, Task):
                    task_id = event.history[0].taskId
                    context_id = event.contextId
                if isinstance(event, TaskStatusUpdateEvent):
                    task_done = event.final
                    if task_done == True:
                        state = event.status.state
                        if state == TaskState.input_required:
                            response = event.status.message.parts[0].root.text
                            types = "Task Status"
                if isinstance(event, TaskArtifactUpdateEvent):
                    response = event.artifact.parts[0].root.text
                    types = "Task Artifact"
        else:
            response_type = "Non-Streaming"
            request_non_stream = SendMessageRequest(
                id=str(uuid4()),
                params=request,
            )
            response = await self.client.send_message(request_non_stream)
            event = response.root.result
            if isinstance(event, Task):
                task_id = event.history[0].taskId
                context_id = event.contextId
                artifact = event.artifacts[0]
                if isinstance(artifact, Artifact):
                    response = artifact.parts[0].root.text
                    types = "Task Artifact"
    
        return {
            "status": True,
            "type": types,
            "responseAgentServer": response_type,
            "message": response,
            "taskId": task_id,
            "contextId": context_id,
        }