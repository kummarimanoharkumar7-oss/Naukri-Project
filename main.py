from flask import Flask
import threading
import asyncio
from uploader import run_uploader

app = Flask(__name__)

@app.route("/")
def home():
    return "Naukri Auto Uploader Running Successfully"

def start_flask():
    app.run(host="0.0.0.0", port=8080)

def start_uploader():
    asyncio.run(run_uploader())

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()
    start_uploader()
