# import requests
# from request import url
# from sqlalchemy import create_engine,text

# engine = create_engine("postgresql://postgres:krishna12345@localhost:5432/argo_2024")
# payload = {"question": ""}

# response = requests.post(url, json=payload)
# response = response.json()

# def returnRows(response):
#     with engine.connect() as conn:
#         result = conn.execute(text(response["sql"]))
#         if result:
#             for row in result:
#                 return row
#         else:
#             return "Data Unavailable"



# # print(response.json())



import requests
from request import url
from sqlalchemy import create_engine,text

engine = create_engine("postgresql://postgres:krishna12345@localhost:5432/argo_2024")
# payload = {"question":"Give me salinity profiles in march 2025"}
# response = requests.post(url, json=payload)
# response = response.json()
def returnRows(response):
    with engine.connect() as conn:
        result = conn.execute(text(response["sql"]))
        if result:
            rows = result.fetchall() # Fetch all rows
            return rows
        else:
            return "Data unavailable" # Return an empty list if no data

def create_chat_history_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                user_query TEXT NOT NULL,
                llm_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

def insert_chat_history(user_query, llm_response):
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO chat_history (user_query, llm_response) VALUES (:user_query, :llm_response)"),
                     {"user_query": user_query, "llm_response": llm_response})
        conn.commit()

# Ensure the table is created when sql_table.py is imported
create_chat_history_table()

# print(response.json())