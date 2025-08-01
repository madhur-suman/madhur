import logging
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from db import get_shop_id_by_phone, execute_query, get_database_schema_info

logger = logging.getLogger(__name__)

class DBChain:
    """
    Converts natural language queries into SQL using LangChain and executes them.
    Now supports filtering queries by phone_number (shop-specific).
    """

    def __init__(self):
        # Initialize LangChain SQL components
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            self.db = SQLDatabase.from_uri("sqlite:///sales.db")
            self.chain = create_sql_query_chain(self.llm, self.db)
        except Exception as e:
            logger.error(f"Error initializing DBChain: {e}")
            raise e

    def run(self, query: str, phone_number: str = None) -> str:
        try:
            # Determine shop filter
            shop_id = get_shop_id_by_phone(phone_number) if phone_number else None

            # Pass DB schema context to LLM
            prompt_with_schema = f"""
            You are a SQL assistant. Convert this natural language query to SQL
            based on the following schema:

            {get_database_schema_info()}

            If shop_id is provided, ensure you filter queries using it:
            shop_id = '{shop_id}' (if None, query all data).

            Query: {query}
            """

            # Generate SQL query from natural language
            sql_query = self.chain.invoke({"question": prompt_with_schema})

            logger.info(f"Generated SQL Query: {sql_query}")

            # Execute query (shop filter handled in execute_query)
            columns, results = execute_query(sql_query, phone_number=phone_number)

            return self.format_response(columns, results)

        except Exception as e:
            logger.error(f"DBChain run error: {e}")
            return f"❌ Error: {e}"

    def format_response(self, columns, results):
        """Format DB results into readable text"""
        if not results:
            return "No results found."

        # Convert to a clean table-like output
        output = []
        for row in results:
            output.append(", ".join([f"{col}: {val}" for col, val in zip(columns, row)]))

        return "\n".join(output)


# Export single instance
db_chain = DBChain()
