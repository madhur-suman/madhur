from db_chain import db_chain

def kirana_qa_pipeline(query: str, phone_number: str = None) -> str:
    """
    Wrapper around DBChain for both WhatsApp and Streamlit.
    """
    try:
        return db_chain.run(query, phone_number=phone_number)
    except Exception as e:
        return f"❌ Error: {e}"
