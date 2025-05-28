from fastapi import FastAPI
from pydantic import BaseModel
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os

from llm import get_llm


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


def get_agent():
    database = os.environ.get("PG_CONNECTION_STR")
    if not database:
        raise ValueError("Environment variable PG_CONNECTION_STR not set")

    db = SQLDatabase.from_uri(database)
    model = get_llm()
    toolkit = SQLDatabaseToolkit(db=db, llm=model)

    print(f"Database dialect: {db.dialect}")
    print(f"Usable tables: {db.get_usable_table_names()}")

    system_message = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables. 

    If your verified query has a long runtime, for example if it takes longer than 20 seconds, 
    only print the query, do not run it.
    """.format(
        dialect="Postgresql",
        top_k=5,
    )

    agent = create_react_agent(model, toolkit.get_tools(), prompt=system_message)
    return agent


agent = get_agent()


def run_agent(x):
    content = ""
    for step in agent.stream(
            {"messages": [{"role": "user", "content": x["input"]}]},
            stream_mode="values",
    ):
        content = step["messages"][-1]
    return {"output": content}


agent_executor = RunnableLambda(run_agent)

app = FastAPI(
    title="LangServe SQL Agent",
    version="1.0",
    description="LangServe app exposing a React agent for SQL querying",
)

add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output).with_config(
        {"run_name": "react_sql_agent"}
    ),
    disabled_endpoints=["batch"],
)

# uvicorn db_serve:app --reload
