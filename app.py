from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
import os

app = Flask(__name__)

# 🔐 Configura esto con tus propios datos:
PROJECT_ID = "TU_PROJECT_ID_AQUI"
LANGUAGE_CODE = "es"
SESSION_ID = "whatsapp-session"
ACCESS_TOKEN = "Bearer ya29.c.c0ASRK0Ga0BUxnA5kaQxoooK7giOEVDKocLaY6qQmfWyznXhHX2jYIZaBEr5tqluc0OFdXE9JgiNm_MikbUe_mPyNSRGgDIeGatEz3RKHx-lrk4IBWChWgd0A7GcibitmEZCr7h6npihY8k2VXCHAOFB85NdI9yZxSM6eE3O9rSpkl4aqrTRpy1IdUTxkjASnGTeSUIUxAdP5d3njo1DETyjUxmE68BIf3i9bPtcsWBx7DBwTfVg8RB1DZjozDBZqT-MuqNMGpFr6Zo-J1Je4TZ20WDz9Lf-o-YiDvkl4RnglS20aUpLmsz6rKcVfm--zc9sbVU86PIXjhvUPSsPfUjUnLHDHNggPv_-yRCMtq2NxuBiqQeEvpLmNHub5s8Zyr8yZ2H397PVrd8W2z_hgIwyd6j9bqO0tpSsmcY-aBoVXjIncUn50woqv_2W96Jq4Zl5h8mhfguh12nxmehYZWxvF-IkzqYhq5f05rfcqrUz-x9ukeyR0hxFYUyb_BrQoa8USispbqBbXpy86QS57526fFXJSwyn1FX2bIb6iQuoJBmV_ZmyenQ5zYejo08_hfboyliRR_uywRoh8rwlwfyuc3vccZYyaWMvV9y66eMvguX0R-pd9SFy4xXbgFcI-YYuqW0Y4yiZyFXr2BfIBl816SocsBRztM09FlJ5BWct_zBddx3snSm2-5_BXp8UJZyRkixF-c5e6MWB6dyrk8b6J9w2aYqt0ihzS8rU3uIVz_bbzR3ydmY2063tlcX5WdgUItOXZgMxrW58ZgY6XJX-g0azZizzoqx53thwgbxFu8IFXahrSallclboytjpuX-oF6-O2OB5-SuStz0nZ2Q7qbh8haRstjapa8k0WZa-vmZVxV200_zvqwRWOy9SSbh5baVYSVIdu-y004XWFUO_gXwVd5iRZz66O2tzzwpvcdsgWe1BS4occBpdYakf7YRbpr18zvUQg1Io6_bY4t-qk3ZUQ5U_ml-g_voFj79Fk5jkl4YjXOOqg"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    phone = request.values.get("From", "")
    print(f"📩 Mensaje recibido: '{incoming_msg}' de {phone}")

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

    try:
        dialogflow_response = requests.post(url, headers=headers, data=json.dumps(body))
        print("📡 Enviado a Dialogflow. Status:", dialogflow_response.status_code)

        if dialogflow_response.status_code != 200:
            print("❌ Error en respuesta:", dialogflow_response.text)
            twilio_response = MessagingResponse()
            twilio_response.message("Error al contactar Dialogflow.")
            return str(twilio_response)

        result = dialogflow_response.json()
        fulfillment_text = result['queryResult']['fulfillmentText']
        print("✅ Respuesta de Dialogflow:", fulfillment_text)

    except Exception as e:
        print("❌ Excepción al procesar:", str(e))
        print("🧾 Respuesta cruda:", dialogflow_response.text if dialogflow_response else "No hay respuesta")
        fulfillment_text = "Error interno al procesar tu mensaje."

    twilio_response = MessagingResponse()
    twilio_response.message(fulfillment_text)
    return str(twilio_response)

@app.route("/", methods=["GET"])
def home():
    return "Webhook activo."

# 👇 Configura para Render: escucha en 0.0.0.0:$PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
