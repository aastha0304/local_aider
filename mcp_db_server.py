from mcp.server.fastmcp import FastMCP
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os


from llm import get_llm

mcp = FastMCP("SQLDatabase")

database_url = os.environ.get("PG_CONNECTION_STR")
if not database_url:
    raise ValueError("Set PG_CONNECTION_STR environment variable")

db = SQLDatabase.from_uri(database_url)
model = get_llm()
toolkit = SQLDatabaseToolkit(db=db, llm=model)  # LLM not needed for tools, but this toolkit needs an LLM

for tool in toolkit.get_tools():
    @mcp.tool(name=tool.name, description=tool.description)
    async def run_tool(*args, tool=tool, **kwargs):
        return tool.invoke(args[0] if args else kwargs)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

# python mcp_db_server.py