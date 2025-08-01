from kirana_qa_pipeline import kirana_qa_pipeline

class AIQueryProcessor:
    """
    Unified AI Query Processor
    - Used by WhatsApp bot (multi-language)
    - Used by Streamlit app (direct queries)
    """

    def __init__(self):
        pass

    def process_query(self, query: str, language: str = 'en', phone_number: str = None) -> str:
        """
        Process query using kirana_qa_pipeline.
        - Translates non-English queries to English (if required)
        - Passes query to kirana_qa_pipeline for execution
        """

        # Simple placeholder for language handling
        # (Later, integrate translation API like Google Translate if needed)
        if language == 'hi':
            # Assume kirana_qa_pipeline expects English; just tag response
            query = f"[Hindi Query] {query}"

        try:
            response = kirana_qa_pipeline(query)
            return response
        except Exception as e:
            return f"❌ Error processing query: {e}"

    def get_sample_questions(self, language='en'):
        """Return sample questions based on language"""
        if language == 'hi':
            return [
                "पिछले हफ्ते सबसे ज्यादा बिकने वाली चीजें कौन सी थीं?",
                "इस महीने का कुल मुनाफा कितना है?",
                "कौन सी चीजें 3 दिनों में एक्सपायर हो रही हैं?"
            ]
        else:
            return [
                "Which item sold the most last week?",
                "What is the total profit for this month?",
                "Which items will expire in the next 3 days?"
            ]
