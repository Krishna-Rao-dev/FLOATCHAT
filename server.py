# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from gemini_sql import generateQuery, prompt

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_sql(req: QueryRequest):
    sql_query = generateQuery(prompt, req.question)
    return {"question": req.question, "sql": sql_query}
