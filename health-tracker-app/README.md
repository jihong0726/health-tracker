# Health Tracker App

A lightweight GitHub + Telegram health tracker for:
- recording daily meals
- recording daily weight
- switching between Ji Hong and Mabel
- viewing historical data across devices
- pushing a daily summary at 12:00 am Malaysia time

## Stack
- Telegram Bot: Python
- Data storage: JSON files in GitHub repo
- Web dashboard: GitHub Pages
- Daily summary: GitHub Actions

## Date and time rules
- Date format: `dd.mm.yyyy` like `13.03.2026`
- Time format: `am / pm`
- Weight format: `72.4 kg`

## Important note
GitHub Pages can host the dashboard and GitHub Actions can send the nightly summary.
But the Telegram bot itself needs a runtime such as Render, Railway, a VPS, or your own computer.

## Setup

### 1. Create Telegram bot
- Create a bot with BotFather
- Copy the bot token

### 2. Get chat IDs
- Start the bot from your Telegram account(s)
- Use `/whoami` to see the current chat ID after deployment

### 3. Configure environment variables for the bot runtime
- `BOT_TOKEN`
- `DEFAULT_PERSON` -> optional, default is `Ji Hong`

### 4. Configure GitHub Actions secrets
Add these repository secrets:
- `BOT_TOKEN`
- `JIHONG_CHAT_ID`
- `MABEL_CHAT_ID`

### 5. Enable GitHub Pages
Publish the `web/` folder with your preferred Pages workflow or static hosting setup.

### 6. Deploy the bot
Deploy the `bot/` folder to:
- Render
- Railway
- VPS
- local always-on machine

## Telegram commands
- `/start`
- `/help`
- `/person`
- `/weight`
- `/meal`
- `/today`
- `/history`
- `/whoami`

## Data files
- `data/weights.json`
- `data/meals.json`

## Midnight summary
The included workflow runs at `16:00 UTC`, which is `12:00 am` Malaysia time.
