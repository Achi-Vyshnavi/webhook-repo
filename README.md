# Webhook-Repo

This repository implements the **GitHub webhook endpoint** for capturing repository events (Push, Pull Request, Merge) and storing them in **MongoDB**. It also serves a minimal **UI** that displays the latest events in real-time.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Repository Structure](#repository-structure)  
- [Setup & Installation](#setup--installation)  
- [Running the Application](#running-the-application)  
- [Testing the Webhook](#testing-the-webhook)  
- [UI](#ui)  
- [MongoDB Schema](#mongodb-schema)  
- [Submission](#submission)  

---

## Overview

This repository acts as the **webhook receiver** for a separate GitHub repository (`action-repo`) where events occur. The webhook listens to the following events:

1. **Push** – Triggered when code is pushed to any branch.  
2. **Pull Request** – Triggered when a pull request is created or updated.  
3. **Merge** – Triggered when a pull request is merged.  

The webhook stores only the **necessary information** in MongoDB and displays it neatly in a UI.

---

## Features

- Receives GitHub webhook events (`push`, `pull_request`).  
- Detects if a pull request was merged.  
- Stores event data in MongoDB with timestamp.  
- Minimal UI that fetches events from MongoDB every 15 seconds.  
- Displays events in the following formats:

| Event Type      | Display Format |
|-----------------|----------------|
| PUSH            | `"author" pushed to "to_branch" on timestamp` |
| PULL_REQUEST    | `"author" submitted a pull request from "from_branch" to "to_branch" on timestamp` |
| MERGE           | `"author" merged branch "from_branch" to "to_branch" on timestamp` |

---

## Repository Structure

webhook-repo/
├─ app.py # Flask application with webhook endpoints
├─ requirements.txt # Python dependencies
└─ templates/
└─ index.html # UI to display events


> No `static/` folder is included, since CSS and JS are embedded in `index.html`.

---

## Setup & Installation

1. Clone the repository:

```bash
git clone <webhook-repo-url>
cd webhook-repo
Create a virtual environment (optional):

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
Install dependencies:

pip install -r requirements.txt
Ensure MongoDB is running on mongodb://localhost:27017/.

Running the Application
python app.py
Flask runs on http://localhost:5000/

Webhook endpoint: POST /webhook

UI to view events: GET / (index.html)

Testing the Webhook
Go to the action-repo repository.

Navigate to Settings → Webhooks → Add webhook.

Set Payload URL to the webhook endpoint:

http://<server-ip>:5000/webhook
Set Content type to application/json.

Select Just the push and pull request events.

GitHub will send events on push, pull request, or merge.

UI
Accessible at http://localhost:5000/.

Displays events in a clean, minimal layout.

Automatically polls MongoDB every 15 seconds for new events.

Example formats:

"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC
MongoDB Schema
Each event document structure:

{
  "type": "PUSH" | "PULL_REQUEST" | "MERGE",
  "author": "username",
  "from_branch": "branch_name",   // only for pull requests and merges
  "to_branch": "branch_name",
  "timestamp": "ISO8601 formatted timestamp"
}
All timestamps are in UTC.

Only minimal, necessary information is stored.
