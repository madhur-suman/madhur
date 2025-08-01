from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from custom_prompt import custom_sql_prompt
from gemini_llm import llm

db = SQLDatabase.from_uri("sqlite:///sales.db")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)