# Content Pipeline — Multi-Agent AI Mini Project

A mini project for an Agentic AI internship submission.

Instead of one prompt producing one output, this app breaks a task into
three specialized agents that hand off work to each other automatically:

```
Topic  →  Research Agent  →  Writer Agent  →  Editor Agent  →  Final Content
```

An **Orchestrator** runs the three agents in order, passes each agent's
output into the next one, and logs every step — so you can watch the
pipeline work stage by stage instead of just seeing one final answer.

Built with **Flask** (backend + frontend in one app) and **Google Gemini**.

---

## Project Structure

```
content-pipeline/
├── app.py                   # Flask app: routes + API
├── agents/
│   ├── gemini_client.py     # Shared Gemini API wrapper
│   ├── research_agent.py    # Agent 1: research & outline
│   ├── writer_agent.py      # Agent 2: drafts content
│   ├── editor_agent.py      # Agent 3: polishes final content
│   └── orchestrator.py      # Coordinates all 3 agents + logging
├── templates/
│   └── index.html           # Frontend page
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── Procfile                 # Tells the hosting platform how to run the app
├── .env.example
└── README.md
```

---

## Part 1 — Install what you need (one-time setup)

You said you don't have Python installed. Here's exactly what to do.

### 1. Install Python
1. Go to https://www.python.org/downloads/
2. Click the yellow **"Download Python"** button (it auto-detects your OS).
3. Run the installer.
   - **Windows:** on the first screen, tick the box **"Add python.exe to PATH"** at the bottom before clicking Install. This step is easy to miss and important.
   - **Mac:** just run through the installer normally.
4. Verify it worked: open a terminal (Command Prompt on Windows, Terminal on Mac) and type:
   ```
   python --version
   ```
   You should see something like `Python 3.12.x`. If it says "not recognized," restart your computer and try again — the PATH change needs a restart to take effect.

### 2. Install VS Code (skip if you already have it)
Download from https://code.visualstudio.com/ and install normally.

### 3. Install Git (needed later for deployment)
Download from https://git-scm.com/downloads and install with all default options.

That's everything. You do **not** need to separately install pandas or
anything else — `pip install -r requirements.txt` (below) installs
everything the project needs automatically.

---

## Part 2 — Run it locally in VS Code

### 1. Unzip the project and open it in VS Code
File → Open Folder → select the `content-pipeline` folder.

### 2. Open a terminal inside VS Code
Menu: Terminal → New Terminal (or `` Ctrl+` ``).

### 3. Create a virtual environment
This keeps this project's packages separate from everything else on your
computer.
```
python -m venv venv
```

Activate it:
- **Windows (Command Prompt):** `venv\Scripts\activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

You'll know it worked because your terminal line now starts with `(venv)`.

### 4. Install the project's dependencies
```
pip install -r requirements.txt
```
This single command installs Flask, the Gemini SDK, and everything else
listed in `requirements.txt`. Nothing else to install manually.

### 5. Get a free Gemini API key
Go to https://aistudio.google.com/apikey, sign in with a Google account,
and click **Create API key**. Copy it.

### 6. Add your key to the project
In the `content-pipeline` folder, copy `.env.example` and rename the copy
to `.env`. Open it and paste your key:
```
GEMINI_API_KEY=your_actual_key_here
```

### 7. Run the app
```
python app.py
```

### 8. Open it in your browser
```
http://127.0.0.1:5000
```
Type a topic, click Generate, and watch all three agents run.

---

## Part 3 — Deploy it so it has a real public link

We'll use **Render** — it's free, doesn't require a credit card, and
supports Flask apps directly. Total time: ~10 minutes.

### Step 1: Put your code on GitHub
Render deploys from a GitHub repository, so your code needs to live there first.

1. Go to https://github.com and create a free account if you don't have one.
2. Click the **+** icon (top right) → **New repository**.
3. Name it `content-pipeline`, keep it **Public**, click **Create repository**.
4. GitHub will show you a page with commands. Instead, it's easier to do
   this in VS Code:
   - Open the terminal in your project folder (same as before).
   - Run these commands one at a time:
     ```
     git init
     git add .
     git commit -m "first commit"
     git branch -M main
     git remote add origin https://github.com/YOUR-USERNAME/content-pipeline.git
     git push -u origin main
     ```
   - Replace `YOUR-USERNAME` with your actual GitHub username. It'll ask
     you to log in to GitHub the first time — follow the on-screen prompts.
5. Refresh your GitHub repository page — you should see all your files there.

> **Important:** Your `.env` file will NOT be uploaded (the `.gitignore`
> file makes sure of that). This is correct and intentional — you never
> want your API key visible on GitHub. You'll add it separately in Render
> in Step 3 below.

### Step 2: Create the Render web service
1. Go to https://render.com and sign up (you can sign up directly with
   your GitHub account — this makes the next step easier).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account if prompted, then select your
   `content-pipeline` repository.
4. Fill in the settings:
   - **Name:** anything you like, e.g. `content-pipeline`
   - **Region:** closest to you
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Don't click "Create" yet — scroll down first (next step).

### Step 3: Add your API key
Still on that same setup page, find **Environment Variables** and click
**Add Environment Variable**:
- **Key:** `GEMINI_API_KEY`
- **Value:** paste your actual Gemini key

(Optionally also add `GEMINI_MODEL` = `gemini-2.0-flash` if you want to be explicit.)

### Step 4: Deploy
Click **Create Web Service**. Render will install your dependencies and
start the app automatically — this takes 2-5 minutes. You'll see live logs
on screen.

### Step 5: Get your link
Once it says **"Live"** at the top, your app is available at a URL like:
```
https://content-pipeline.onrender.com
```
That's your public link — open it, and it works exactly like it did on
your `127.0.0.1:5000` locally, except anyone can now access it.

> **Note on the free tier:** Render's free web services "sleep" after 15
> minutes of no traffic and take ~30-50 seconds to wake up on the next
> visit. This is normal — just let it load. If your submission requires
> zero delay, mention this in your report; it's a well-known free-tier
> behavior, not a bug in your code.

---

## How It Works (for your report / viva)

1. The user submits a topic, content type, tone, and length via the form.
2. `app.py` receives the request at `POST /api/generate` and calls
   `orchestrator.run_pipeline()`.
3. The **Research Agent** calls Gemini with a research-focused system
   prompt and returns key points, a suggested outline, and an angle.
4. The **Writer Agent** receives that research as context and calls Gemini
   again with a writer-focused system prompt to produce a first draft.
5. The **Editor Agent** receives the draft and calls Gemini with an
   editor-focused system prompt to polish it and list what it changed.
6. The orchestrator logs each handoff with a timestamp and returns all
   three agents' outputs plus the log to the frontend.
7. The frontend renders the agent log and each stage's output separately,
   so the multi-agent flow is visible — not just the final result.

---

## Why this counts as agentic AI

| Trait | How this project shows it |
|---|---|
| Task decomposition | One goal split into research → write → edit sub-tasks |
| Role specialization | Each agent has its own system prompt and single job |
| Autonomous handoff | Orchestrator passes outputs between agents with no manual step |
| Observable reasoning trace | The activity log shows the pipeline's steps in order |

---

## Troubleshooting

- **"GEMINI_API_KEY is missing"** — you created `.env.example` but not
  `.env`. Make a copy and rename it to exactly `.env`.
- **502 error / Gemini API call failed** — your API key is invalid, or
  you've hit the free-tier quota. Double-check the key was copied fully.
- **`python` not recognized** — Python wasn't added to PATH during
  install. Reinstall and tick "Add python.exe to PATH", then restart
  your computer.
- **Render build fails** — check the build logs on the Render dashboard;
  the most common cause is a typo in the Start Command (`gunicorn app:app`).
- **Site loads but says "Application Error" on Render** — double check
  the `GEMINI_API_KEY` environment variable is set correctly in the
  Render dashboard (not just in your local `.env` file — Render can't see
  your local file).
