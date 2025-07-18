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
ACCESS_TOKEN = "Bearer ya29.c.c0ASRK0GYSibsuPhfcGjvch8kReUrRzsNE0GlB7NwMxDEdDnAPqBvunzLWy7T9GDri7TMicfh_bHgaziyuIYtt2SCP8DLaNrT6r3NyIR-6Q8EcE9ITHCOD1zz6GdW6xuXfUxhcSMvvzf45eqzumJVNlQCdw3ZjuUOkIMiAr53wCJkfcJzejfZiOkwI6lvtY-JZEJFaBAN2qbiWBp3Pg2lRGMnXXj_yA-hubw2ZL_0sg8CHbZJhjHOwundXPVPD7IrlXHxDrsmarxM09MBk0yEOiz14gDeBcIsuUvQWb-yM5Iji4E7iHCDjd2LF6ZfapNZ1MwwAXj5xClrgbAubZbiuM9KzAXBxkwWXGk4Dy9OLVdW73Fei1smwD6kMvuMDdd3oAG0D5LUT400C8_jBVnUbpsQknBUUgu7cr11-JRqqVJau5YtFuao9OwOkfXoU2m5MYZ3SccZf42_xcWiqIXXeW1p0UfF-3kMctaMakix_RgRwVsQrvolSJ1y7FQjSYJW-wda7x8m3FZaos1dd7_vuirun051h3w-8ognB1bfm44q6lwM0oQzQUqz0O1RhWc_rt28gaxQhgJ_7X9MYkhO7Rqdhgly9v--hqBgliRZ0FRmk_i55Ocuuu6W6bfbW30l-_O-xYJdBw3hycbv0vXgx7uozhggkjxirppZ6Fe86_cOYZRi_Oi0l526u-gkOSsnFQ82b114Rt7Bcf8_1MuRW_pU5behY-OrBe048r1pmnQtxjXzmMkUQ7-MV4arZneIx-IJa0t328iiQ197nX1v99l029g5h-IVz8FeaV5Y9c-2ajR1y_w3QybVpl5mm4sY7cSungcSvO9qRp_s4hWicJSptYrp_hbzp7imaYf65rdQ8-qsgQ2lBVRfBtunusO4Xt38w3YVkzpWz20ayVB9tMQxz5a_Y0X1xFFiwl1tZk0zVZXyY18xUB_SvaJqt1n5pqs-5-60U8MSzk9ioYs1xz4M3XOpXoqn72BVcekgv0hcp7qwe7M4u2si"

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
