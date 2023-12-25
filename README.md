# Contextual Context Extraction -> Chatbot:


### What it does:
   
- Read in input from either (1) url link or (2) text file (.txt, .md, .docx, ... . No image/pdf file yet) 
- Split the input into smaller document chunks
- Store vectorised data inside the vector database
- When the user send a query, return the most relevant document chunk 
- Extra: store session history in SQL, and send context + history to GPT for the final touch


### Tech stack:
 - Pipelining: Towhee
 - Front end: Gradio
 - Back end: Fastapi
 - Vector DB: Milvus
 - SQL DB: Postgres
 - LLM: GPT
 - Cloud: GCP

### Installation:
- install postgres
- install [milvus](https://milvus.io/docs/v2.1.x/install_standalone-docker.md), for GCP use [this resource](https://milvus.io/docs/gcp.md)
- clone the repo
- create the required .env file based on `config.py`
- if `docker compose up -d` does not work for backend component:
  - create & install the requirements for each 
  - server: `uvicorn main:app`
  - client: `python3 app.py`

### Known Issue:
- If failed to install psycopg2 for posgres, `sudo apt-get install libpq-dev`
- No GPU attached, so all the related issues with it
