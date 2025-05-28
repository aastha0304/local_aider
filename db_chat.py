from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import os

from llm import get_llm

memory = MemorySaver()


def get_agent():
    database = os.environ.get('PG_CONNECTION_STR')
    db = SQLDatabase.from_uri(database)

    model = get_llm()
    toolkit = SQLDatabaseToolkit(db=db, llm=model)

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

    agent = create_react_agent(model, toolkit.get_tools(), prompt=system_message, checkpointer=memory)
    return agent


if __name__ == '__main__':
    config = {"configurable": {"thread_id": "db_chat_thread"}}
    agent_executor = get_agent()
    while True:

        question = input("> ")

        for step in agent_executor.stream(
                {"messages": [{"role": "user", "content": question}]},
                stream_mode="values",
                config=config,
        ):
            step["messages"][-1].pretty_print()
