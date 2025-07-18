from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

# CONFIGURA ESTOS VALORES
PROJECT_ID = "tu_project_id_de_dialogflow"
LANGUAGE_CODE = "es"
SESSION_ID = "whatsapp-session"
ACCESS_TOKEN = "Bearer tu_token_de_dialogflow"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    phone = request.values.get("From", "")
    
    # Dialogflow API call
    url = f"https://dialogflow.googleapis.com/v2/projects/{PROJECT_ID}/agent/sessions/{SESSION_ID}/detectIntent"
    headers = {
        "Authorization": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    body = {
        "queryInput": {
            "text": {
                "text": incoming_msg,
                "languageCode": LANGUAGE_CODE
            }
        }
    }

    dialogflow_response = requests.post(url, headers=headers, data=json.dumps(body))
    result = dialogflow_response.json()
    fulfillment_text = result['queryResult']['fulfillmentText']

    # Twilio reply
    twilio_response = MessagingResponse()
    twilio_response.message(fulfillment_text)
    return str(twilio_response)

@app.route("/", methods=["GET"])
def health():
    return "Webhook activo."

if __name__ == "__main__":
    app.run(debug=True)
