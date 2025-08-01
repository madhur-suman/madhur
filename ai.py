import logging
from db_chain import db_chain

logger = logging.getLogger(__name__)

class AIQueryProcessor:
    """
    AIQueryProcessor using Gemini via DBChain.
    Handles natural language queries and converts them to SQL.
    """

    def __init__(self):
        # Initialization (no Hugging Face / BharatGPT)
        logger.info("AIQueryProcessor initialized with Gemini backend")

    def process_query(self, query: str, language: str = 'en', phone_number: str = None) -> str:
        """
        Process a query using DBChain (Gemini).
        """
        try:
            logger.info(f"Processing query with Gemini: {query}")
            return db_chain.run(query, phone_number=phone_number)
        except Exception as e:
            logger.error(f"AI processing failed: {e}")
            return f"I encountered an error while processing your query: {e}"

    def get_sample_questions(self, language: str = 'en'):
        """
        Provide sample queries to help users.
        """
        samples_en = [
            "Which item sold the most last week?",
            "Total profit for this month?",
            "Which items will expire in 3 days?",
            "Top 5 selling items?",
            "Profit from milk sales?"
        ]
        samples_hi = [
            "पिछले हफ्ते सबसे ज्यादा क्या बिका?",
            "इस महीने का कुल मुनाफा कितना है?",
            "अगले 3 दिनों में कौन सी चीजें एक्सपायर होंगी?",
            "टॉप 5 बिकने वाली चीजें कौन सी हैं?",
            "दूध की बिक्री से कितना मुनाफा हुआ?"
        ]
        return samples_hi if language == 'hi' else samples_en
