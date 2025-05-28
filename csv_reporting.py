import os

import pandasai as pd_ai
from llm import get_llm_pandasai

pd_ai.api_key.set(os.environ['PANDASAI_API_KEY'])

model = get_llm_pandasai()
pd_ai.config.set({"llm": model})


def quickstart():
    df = pd_ai.read_csv("./local_data/diabetes.csv")

    while True:
        # Is there context?
        # q1 = "What is the minimum age in the dataset of diabetes?"
        # q1 = "And what is the maximum?"
        # Can it do visualization?
        # q1 = "Plot the histogram of age distribution from the diabetes dataset. You can use buckets of 5."
        # It cannot describe data for you
        q1 = input()
        response = df.chat(q1)
        print(response)


if __name__ == '__main__':
    quickstart()

