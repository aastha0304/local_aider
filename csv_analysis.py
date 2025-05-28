from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain import hub
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import pandas as pd
from sqlalchemy import create_engine

from llm import get_llm

df_data = pd.read_csv("./local_data/diabetes.csv")
# df_submissions = pd.read_json("./local_artifacts/diabetes_code_submissions.json")

engine = create_engine("sqlite:///local_aider.db")
df_data.to_sql("diabetes_data", engine, index=False, if_exists='replace')
# df_submissions.to_sql("diabetes_code_submissions", engine, index=False, if_exists='replace')
db = SQLDatabase(engine=engine)

llm = get_llm()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

sql_tools = toolkit.get_tools()

tools = [sql_tool for sql_tool in sql_tools]

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

system_message = prompt_template.format(dialect="SQLite", top_k=100)
system_message += """

You are an intelligent data processing agent. You have the following tools to use from:
1 SQLDatabaseToolkit : To query tables in SQLite database
2 PythonREPLTool : To execute Python code for data processing, analysis, or visualization. Make sure to run the code not just print it.
3 WriteFileTool : To write the files out into local filesystem

When querying the database tables use all the data to generate correct responses.
Use all the tools available to you answer the user and save files where the user so requires.
"""

memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, checkpointer=memory) #, prompt=system_message)

config = {"configurable": {"thread_id": "abc123"}}

# question = "What is the maximum age in diabetes_data table?"
#
# for step in agent_executor.stream(
#         {"messages": [{"role": "user", "content": question}]},
#         config=config,
#         stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()
#
# question = "And what is the minimum?"
#
# for step in agent_executor.stream(
#         {"messages": [{"role": "user", "content": question}]},
#         config=config,
#         stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()
#
# question = "What is the DDL for diabetes_data table ?"
#
# for step in agent_executor.stream(
#         {"messages": [{"role": "user", "content": question}]},
#         config=config,
#         stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()
#
# question = "What is the DDL for diabetes_submissions table ?"
#
# for step in agent_executor.stream(
#         {"messages": [{"role": "user", "content": question}]},
#         config=config,
#         stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()

while True:
    question = input("Your query:")
    # question = "Generate a visualisation of age distribution from diabetes_data table and save it as an svg file"
    for step in agent_executor.stream(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
            stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
