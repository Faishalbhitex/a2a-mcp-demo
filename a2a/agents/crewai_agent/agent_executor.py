from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    InvalidParamsError,
    Part,
    Task,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_artifact,
    completed_task,
)
from a2a.utils.errors import ServerError
from agent import CrewAIAgent

class CrewAIAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = CrewAIAgent()
    
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())
        
        query = context.get_user_input()
        try:
            result = self.agent.invoke(query, context.context_id)
            print(f"Final Result ===> {result}")
        except Exception as e:
            print('Error invoking agent: %s', e)
            raise ServerError(
                error=ValueError(f'Error invoking agent', e)
            ) from e
        
        parts = [Part(root=TextPart(text=result))]
        
        await event_queue.enqueue_event(
            completed_task( 
                context.task_id,
                context.context_id,
                [new_artifact(parts, f'crewai_{context.task_id}')],
                [context.message]
            )
        )

    async def cancel(self, request: RequestContext, event_queue: EventQueue) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
    
    def _validate_request(self, context: RequestContext) -> bool:
        return False