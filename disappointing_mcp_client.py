import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from llm import get_llm


async def main():
    client = MultiServerMCPClient(
        {
            "sql_db": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    # Start a session with the MCP server
    async with client.session("sql_db") as session:
        # Load MCP tools as LangChain tools
        tools = await load_mcp_tools(session)

        # Initialize your LLM (replace with your preferred model)
        llm = get_llm()

        # Create a React agent with the MCP tools
        agent = create_react_agent(llm, tools)

        # Query the agent
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "What is the row count of artist table?"}]},
            config={"recursion_limit": 50}
        )
        print("Agent response:", response)

if __name__ == "__main__":
    asyncio.run(main())