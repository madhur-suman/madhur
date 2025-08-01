from db_chain import db_chain

def kirana_qa_pipeline(query: str) -> str:
    try:
        response = db_chain.run(query)
        return response
    except Exception as e:
        return f"❌ Error: {e}"