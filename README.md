# Local AIDER

**AI for the Data Engineer using Local LLMs**

#### Sample data Setups:

**Postgres**

```angular2html
docker run --name postgres_db -e POSTGRES_PASSWORD=mysecretpassword -v "$(pwd)":/var/lib/postgresql/data -p 5433:5432 -d postgres

docker exec -it postgres_db bash
su - postgres

psql
\i /var/lib/postgresql/data/Chinook_PostgreSql.sql


```

**Python modules**
Apart from usual `pip install -r requirements.txt`
Install playwright to work with web apps and browsers

```angular2html
playwright install
```

#### Very DE specific Remarks 

- Good scraping framework with 10k reader tokens [Jina-AI](https://github.com/jina-ai)
- Brilliant framework for scraping but limited tokens (1200 a month) [AgentQL](https://github.com/tinyfish-io/agentql)
- CSV text based analysis 
  - Good ol' Langchain SQLDatabaseToolkit
    - However, still hiccups with command syntax based on the SQLLite
    - Local models can get crazy when 'overworked', sometimes switching to Groq helps
- Visualization
  - PandasAI is a good tool, using LiteLLM you can use it for as many calls.
- DB table analysis
  - Langchains toolkit can generate catalogs, ERDs in text
  - It can also discover the tables on its own
- DB table visualizations
  - PandasAI can similarly do the job, but it needs individual table declarations
  - PandasAI has good debugging logs that help with understanding the query.
- Observability
  - The Langchain ecosystem- [Langsmith](https://smith.langchain.com/o/e5ae4cfd-cc0e-4f54-b42e-e53e5bb74578/projects/p/f1903479-a54a-4ad6-8974-dd3e5ce268d1?timeModel=%7B%22duration%22%3A%227d%22%7D) provides a comprehensive UI for understanding how the LLM fared
  - It can be extended to business data as well (but not a good idea)
- Serving
  - Again using the Langchain framework ([Langserve](http://127.0.0.1:8000/docs))
- Leveraging MCP
  - Langchain comes with adapters for easy creation of MCP servers and clients

#### Very local-LLM specific remarks
- My local setup is ollama based, qwen 2.5 has been a reliable LLM
- Langchain and Groq also have their chat platforms to help with using them
- I have a fine machine (M3, 18 GB) that can run the above decently.
  - If the machine can't take this workload, try using [Groq](https://groq.com/) (you need to get API keys here too)
```angular2html
llm = init_chat_model("Qwen-Qwq-32b", model_provider="groq")
```
- If you need uncensored models (to understand what AI really thinks of us) you can use dolphin versions of the models.
- It does boil down to the model and prompts.

#### Very Software Engineering specific remarks
- As with all open source models, version hell is a reality.
- Python 3.11 is the best common-ground Python version to work with these frameworks.