import asyncio
import os
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatOpenAI()

# Information on how to run the mcp-server:
stdio_server_params = StdioServerParameters(
    command="python",
    args=[
        "/home/brunojaime/Documents/Projects/mcp-langgraph-client/servers/math_servers.py"
    ],
)


async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)
            print(tools)

            agent = create_react_agent(llm, tools)
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 2+2?")]}
            )
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
