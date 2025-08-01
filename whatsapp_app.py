from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from config import Config
from db import create_database_schema
from expiry_alert import setup_cron_job, send_expiry_alerts
from kirana_qa_pipeline import kirana_qa_pipeline
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Twilio client
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

# In-memory storage for user language preferences (use DB in prod)
user_languages = {}

# Language messages
MESSAGES = {
    'en': {
        'welcome': """🤖 *Sales Analytics Bot*

Choose your preferred language:

1️⃣ English  
2️⃣ हिंदी

Reply with 1 or 2 to select.""",
        'help': """Ask me anything about your inventory or sales. Examples:

• "Which item sold the most last week?"
• "Add 10 Maggi"
• "Remove 5 detergents"
• "Which items expire in 3 days?" 

Type 'help' anytime for this message.
Type 'language' to change language.""",
        'language_changed': "✅ Language changed to English!",
        'error': "Sorry, I encountered an error. Please try again."
    },
    'hi': {
        'welcome': """🤖 *सेल्स एनालिटिक्स बॉट*

अपनी भाषा चुनें:

1️⃣ English  
2️⃣ हिंदी

जवाब में 1 या 2 भेजें।""",
        'help': """इन्वेंटरी या सेल्स के बारे में कुछ भी पूछें। उदाहरण:

• "पिछले हफ्ते सबसे ज्यादा क्या बिका?"
• "10 मैगी जोड़ो"
• "5 डिटर्जेंट हटाओ"
• "कौनसी चीजें 3 दिन में एक्सपायर होंगी?"

किसी भी समय 'help' टाइप करें।
भाषा बदलने के लिए 'language' टाइप करें।""",
        'language_changed': "✅ भाषा हिंदी में बदल दी गई!",
        'error': "माफ़ करें, एक त्रुटि आई। कृपया फिर से कोशिश करें।"
    }
}

def get_user_language(number):
    return user_languages.get(number, 'en')

def set_user_language(number, lang):
    user_languages[number] = lang

def get_message(key, lang='en'):
    return MESSAGES.get(lang, MESSAGES['en']).get(key, MESSAGES['en'][key])

@app.route('/')
def home():
    return jsonify({
        "message": "WhatsApp Sales Analytics Bot",
        "status": "running",
        "endpoints": {
            "webhook": "/whatsapp",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Main WhatsApp webhook"""
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')

        if from_number.startswith('whatsapp:'):
            phone_number = from_number.split('whatsapp:')[1]
        else:
            phone_number = from_number

        logger.info(f"Message from {phone_number}: {incoming_msg}")

        resp = MessagingResponse()
        msg = resp.message()
        user_lang = get_user_language(phone_number)

        # Handle language setup
        if not incoming_msg:
            msg.body(get_message('welcome', user_lang))
            return str(resp)

        if incoming_msg in ['1', '2']:
            selected = 'en' if incoming_msg == '1' else 'hi'
            set_user_language(phone_number, selected)
            msg.body(get_message('language_changed', selected))
            return str(resp)

        if incoming_msg.lower() in ['language', 'भाषा', 'lang']:
            msg.body(get_message('welcome', user_lang))
            return str(resp)

        if incoming_msg.lower() in ['help', 'h', '?', 'मदद']:
            msg.body(get_message('help', user_lang))
            return str(resp)

        # Expiry alert trigger
        if incoming_msg.lower() in ['expiry', 'expire', 'एक्सपायरी']:
            msg.body("Sending expiry alerts..." if user_lang == 'en' else "एक्सपायरी अलर्ट भेजे जा रहे हैं...")
            threading.Thread(target=send_expiry_alerts).start()
            return str(resp)

        # **Pass every other message to kirana_qa_pipeline**
        response = kirana_qa_pipeline(incoming_msg, phone_number)
        msg.body(response)
        return str(resp)

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        resp = MessagingResponse()
        resp.message(get_message('error'))
        return str(resp)

@app.route('/send-message', methods=['POST'])
def send_message():
    """Send a message manually via API"""
    data = request.get_json()
    to_number = data.get('to')
    message = data.get('message')

    if not to_number or not message:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    sent = twilio_client.messages.create(
        from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
        body=message,
        to=f'whatsapp:{to_number}'
    )
    return jsonify({"success": True, "sid": sent.sid, "status": sent.status})

if __name__ == '__main__':
    create_database_schema()
    setup_cron_job()
    app.run(host='0.0.0.0', port=5001, debug=Config.DEBUG)
