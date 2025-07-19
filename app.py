from flask import Flask, request
import requests, time, threading, random

app = Flask(__name__)
sending = False

def send_loop():
    global sending
    with open("token.txt") as f: tokens = f.read().splitlines()
    with open("convo.txt") as f: ids = f.read().splitlines()
    with open("messages.txt") as f: messages = f.read().splitlines()
    with open("time.txt") as f: delay = float(f.read().strip())
    while sending:
        for token in tokens:
            for uid in ids:
                msg = random.choice(messages)
                url = f"https://graph.facebook.com/v18.0/{uid}/messages"
                headers = {"Authorization": f"Bearer {token}"}
                data = {"message": {"text": msg}}
                r = requests.post(url, json=data, headers=headers)
                print(f"[{r.status_code}] Sent to {uid} -> {msg}")
                time.sleep(delay)
        time.sleep(5)

@app.route("/")
def home():
    return open("templates.html").read()

@app.route("/upload", methods=["POST"])
def upload():
    request.files['token'].save("token.txt")
    request.files['convo'].save("convo.txt")
    request.files['messages'].save("messages.txt")
    delay = request.form.get("delay", "2")
    with open("time.txt", "w") as f:
        f.write(delay)
    return "✅ Uploaded. <a href='/'>Back</a>"

@app.route("/start", methods=["POST"])
def start():
    global sending
    if not sending:
        sending = True
        threading.Thread(target=send_loop).start()
    return "🚀 Started! <a href='/'>Back</a>"