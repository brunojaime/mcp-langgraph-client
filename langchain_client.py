from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI()

async def main():
    # Option 1: Create client without context manager
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [
                    "/home/brunojaime/Documents/Projects/mcp-langgraph-client/servers/math_servers.py"
                ],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    )
    
    # Now you can use the client directly
    tools = await client.get_tools()
    print(tools)
    
    agent = create_react_agent(llm,tools)
    result = await agent.ainvoke({"messages":[HumanMessage(content="What is the weather like in Puerto Madryn?")]})
    print(result["messages"][-1].content)



if __name__ == "__main__":
    asyncio.run(main())
