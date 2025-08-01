import streamlit as st
from kirana_qa_pipeline import kirana_qa_pipeline

st.set_page_config(page_title="Kirana Inventory RAG with Gemini + SQL")
st.title("🛒 Kirana Inventory Assistant")

query = st.text_input("Ask something like:\n- Add 10 Maggi\n- How many biscuits left?\n- Remove 5 detergents")

if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        result = kirana_qa_pipeline(query)
    st.markdown("### Response:")
    st.write(result)