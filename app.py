from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

# CONFIGURA ESTOS VALORES
PROJECT_ID = "faq-bot-ksdg"
LANGUAGE_CODE = "es"
SESSION_ID = "whatsapp-session"
ACCESS_TOKEN = "Bearer ya29.c.c0ASRK0GYSibsuPhfcGjvch8kReUrRzsNE0GlB7NwMxDEdDnAPqBvunzLWy7T9GDri7TMicfh_bHgaziyuIYtt2SCP8DLaNrT6r3NyIR-6Q8EcE9ITHCOD1zz6GdW6xuXfUxhcSMvvzf45eqzumJVNlQCdw3ZjuUOkIMiAr53wCJkfcJzejfZiOkwI6lvtY-JZEJFaBAN2qbiWBp3Pg2lRGMnXXj_yA-hubw2ZL_0sg8CHbZJhjHOwundXPVPD7IrlXHxDrsmarxM09MBk0yEOiz14gDeBcIsuUvQWb-yM5Iji4E7iHCDjd2LF6ZfapNZ1MwwAXj5xClrgbAubZbiuM9KzAXBxkwWXGk4Dy9OLVdW73Fei1smwD6kMvuMDdd3oAG0D5LUT400C8_jBVnUbpsQknBUUgu7cr11-JRqqVJau5YtFuao9OwOkfXoU2m5MYZ3SccZf42_xcWiqIXXeW1p0UfF-3kMctaMakix_RgRwVsQrvolSJ1y7FQjSYJW-wda7x8m3FZaos1dd7_vuirun051h3w-8ognB1bfm44q6lwM0oQzQUqz0O1RhWc_rt28gaxQhgJ_7X9MYkhO7Rqdhgly9v--hqBgliRZ0FRmk_i55Ocuuu6W6bfbW30l-_O-xYJdBw3hycbv0vXgx7uozhggkjxirppZ6Fe86_cOYZRi_Oi0l526u-gkOSsnFQ82b114Rt7Bcf8_1MuRW_pU5behY-OrBe048r1pmnQtxjXzmMkUQ7-MV4arZneIx-IJa0t328iiQ197nX1v99l029g5h-IVz8FeaV5Y9c-2ajR1y_w3QybVpl5mm4sY7cSungcSvO9qRp_s4hWicJSptYrp_hbzp7imaYf65rdQ8-qsgQ2lBVRfBtunusO4Xt38w3YVkzpWz20ayVB9tMQxz5a_Y0X1xFFiwl1tZk0zVZXyY18xUB_SvaJqt1n5pqs-5-60U8MSzk9ioYs1xz4M3XOpXoqn72BVcekgv0hcp7qwe7M4u2si"

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
