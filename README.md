Webhook Repo - GitHub Event Listener

This repository implements a GitHub webhook receiver that listens for events from another repository (action-repo) and stores them in MongoDB. The events are then displayed in a clean UI that polls the database every 15 seconds.

This repo fulfills the Developer Assessment Task requirements for capturing GitHub actions ("Push", "Pull Request", "Merge") and rendering them to the UI.

Repo Structure
webhook-repo/
│
├── app.py                # Flask backend server
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend UI to display events
└── README.md             # This file


Note: The static/ folder is not required, as all CSS and JavaScript are embedded in index.html.

Features

Webhook Receiver

Listens for GitHub webhook events:

push → stored as PUSH

pull_request → stored as PULL_REQUEST

pull_request with action=closed and merged=true → stored as MERGE

Stores the minimal necessary data in MongoDB:

author (user who triggered the event)

to_branch (branch targeted)

from_branch (source branch, if applicable)

timestamp (UTC)

MongoDB Storage

MongoDB is used to persist webhook events.

Collection: events in database: github_webhooks.

Example document:

{
  "type": "PUSH",
  "author": "Travis",
  "to_branch": "master",
  "from_branch": "",
  "timestamp": "2026-01-31T12:00:00Z"
}


Frontend UI

Displays events in a clean, minimal design.

Automatically polls /events route every 15 seconds.

Formats timestamps in readable UTC format (with st, nd, rd, th suffixes).

Ngrok Support (Optional)

For local development, expose the Flask server to GitHub via ngrok:

ngrok http 5000


Use the generated public URL in GitHub webhook settings.

Setup Instructions

Clone Repository

git clone <webhook-repo-url>
cd webhook-repo


Install Python Dependencies

pip install -r requirements.txt


Ensure MongoDB is Running

Default connection: mongodb://localhost:27017/

Database: github_webhooks

Collection: events

Start MongoDB locally or use a cloud service (MongoDB Atlas).

Run the Flask Server

python app.py


Server runs on: http://localhost:5000/

Access Frontend UI

Open: http://localhost:5000/

The events will load dynamically and refresh every 15 seconds.

Set Up GitHub Webhook

Go to your action-repo → Settings → Webhooks → Add webhook

Payload URL: <ngrok-or-local-url>/webhook

Content type: application/json

Select individual events: Push, Pull Request

Save the webhook.

Example Event Formats in UI

Push

"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC


Pull Request

"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC


Merge

"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC

Requirements

Create a requirements.txt file with the following:

Flask==2.3.2
pymongo==4.7.1
dnspython==3.8.0   # Only if using MongoDB Atlas

Notes

All frontend scripts and styles are embedded in index.html.

MongoDB must be accessible to the Flask server.

Use ngrok or similar tool to expose local server for GitHub webhook testing.
