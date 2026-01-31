from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.github_webhooks
collection = db.events
@app.route('/')
def home():
    return render_template("index.html")  # Make sure index.html is in templates folder
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event", "").lower()

    print("Received webhook event:", event_type)
    print("Payload:", data)

    doc = None

    try:
        if event_type == "push":
            author = data.get("pusher", {}).get("name") or data.get("sender", {}).get("login")
            to_branch = (data.get("ref") or "").split("/")[-1]
            doc = {
                "type": "PUSH",
                "author": author,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow()
            }

        elif event_type == "pull_request":
            author = data.get("sender", {}).get("login")
            from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = data.get("pull_request", {}).get("base", {}).get("ref")
            if data.get("action") == "closed" and data.get("pull_request", {}).get("merged"):
                doc = {
                    "type": "MERGE",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": datetime.utcnow()
                }
            else:
                doc = {
                    "type": "PULL_REQUEST",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": datetime.utcnow()
                }

        if doc:
            collection.insert_one(doc)
            print(f"Saved event: {doc['type']} by {doc['author']}")
            return "Webhook received", 200
        else:
            return "Event ignored", 200

    except Exception as e:
        print("Error processing webhook:", e)
        return "Error", 500
@app.route('/events')
def get_events():
    events = []
    for e in collection.find().sort("timestamp", -1):
        doc = {
            "type": e.get("type", "UNKNOWN"),
            "author": e.get("author", "Unknown"),
            "to_branch": e.get("to_branch", ""),
            "from_branch": e.get("from_branch", ""),
            "timestamp": e.get("timestamp").isoformat() if isinstance(e.get("timestamp"), datetime) else str(e.get("timestamp"))
        }
        events.append(doc)
    return jsonify(events)
if __name__ == "__main__":
    app.run(port=5000)
