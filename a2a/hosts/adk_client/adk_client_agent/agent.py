import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from a2a_host import A2AADKAgentClient


load_dotenv()
nest_asyncio.apply()


adk_url = os.getenv('ADK_AGENT')
crewai_url = os.getenv('CREWAI_AGENT')
langgraph_url = os.getenv('LANGGRAPH_AGENT')
agent_urls = [adk_url, crewai_url, langgraph_url]

def _init_root_agent():
    async def _async_main():
        client_tools = await A2AADKAgentClient().create(agent_urls=agent_urls)
        return client_tools.create_agent()
    return asyncio.run(_async_main())


root_agent = _init_root_agent()