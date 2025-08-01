from langchain_google_vertexai import VertexAI
import vertexai

vertexai.init(project="gen-lang-client-0960849134", location="global")

llm = VertexAI(
    model_name="gemini-2.5-flash-lite",
    temperature=0.7,
    max_output_tokens=3000
)