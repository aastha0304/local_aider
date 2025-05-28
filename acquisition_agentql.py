from langchain_agentql.tools import ExtractWebDataTool
from langgraph.prebuilt import create_react_agent
from langchain.load import dumps
from llm import get_llm_bind_support


def diabetes_code_submissions():
    url = 'https://www.kaggle.com/datasets/mathchi/diabetes-data-set/code?datasetId=818300&sortBy=voteCount'
    model = get_llm_bind_support()

    extract_web_data = ExtractWebDataTool(is_scroll_to_bottom_enabled=True)

    agent_executor = create_react_agent(model, [extract_web_data])
    user_input = f"""
    Scrape code submissions from this page: {url}. Find all code submissions, be sure to scroll till the end and wait for further loading.
    Extract the columns for: Title | URL | Date | Author | Votes and write this data in a new JSON file called kaggle_code_submissions.json.
    """

    # Execute agent
    events = agent_executor.stream(
        {"messages": [("user", user_input)]},
        stream_mode="values",

    )
    with open('./local_artifacts/diabetes_code_submissions.json', 'a', encoding='utf-8') as f:
        for event in events:
            #   event["messages"][-1].pretty_print()
            f.write(dumps(event["messages"][-1]))


diabetes_code_submissions()
