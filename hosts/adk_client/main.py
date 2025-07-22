import os
import asyncio
from dotenv import load_dotenv
import logging
from adk_client_agent.a2a_host import A2AADKAgentClient


# Disable Log
import google.adk
import google.genai
logging.getLogger("google_adk").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("google_genai.types").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


load_dotenv()

adk_url = os.getenv('ADK_AGENT')
crewai_url = os.getenv('CREWAI_AGENT')
langgraph_url = os.getenv('LANGGRAPH_AGENT')
agent_urls = [adk_url, crewai_url, langgraph_url]


async def main():
    a2a_adk_client = await A2AADKAgentClient.create(agent_urls=agent_urls)
    agent = a2a_adk_client.create_agent()
    print("#------- Start Agent ADK Host -------#")
    while True:
        query = input("\n<<< User Input: ")
        if query.lower().strip() in ["exit", "quit", "keluar", "q"]:
            print("\n<<< Exit")
            break

        async for output in a2a_adk_client.stream(agent=agent, msg=query):
            print(output)

    await a2a_adk_client.close()
    print("#------- End Agent ADK Host -------#")


if __name__ == '__main__':
    asyncio.run(main())
