from .host_agent import HostAgent
import httpx
import asyncio
import nest_asyncio


httpx_client = httpx.AsyncClient(timeout=30)


root_agent = HostAgent(['http://localhost:10001', 'http://localhost:10003'], httpx_client).create_agent()