# Python Scripts

A collection of small Python automation tools — mostly built for real problems around running Sevva Cloud, plus a few learning exercises along the way.

## Scripts

### `emailer.py`
Command-line email sender. Takes a recipient, subject, and message body and sends an email via Gmail SMTP (`smtplib`).

```bash
python3 emailer.py recipient@example.com "Subject line" "Message body"
```

Requires a Gmail account with 2-Step Verification and an [App Password](https://myaccount.google.com/apppasswords) — set as `APP_PASSWORD` in the script (or better, as an environment variable, see Setup below).

### `read_emails_CSV.py`
Analyzes exported Brevo email relay logs (CSV) and reports delivery health — sent/delivered/error rates, top error sources by sender and recipient domain, and daily error trends.

```bash
python3 read_emails_CSV.py path/to/export.csv
```



## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Don't commit credentials or data exports. This repo's `.gitignore` excludes `*.csv` and should exclude any file containing API keys, tokens, or passwords. Use environment variables or a gitignored `.env` file for secrets instead of hardcoding them.

## Notes

These are personal tools, built incrementally while learning Python — not polished packages. Error handling and structure improve as the scripts get reused, not necessarily on the first version.