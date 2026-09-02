# Python Scripts

A collection of small Python automation tools — mostly built for real problems around running Sevva Cloud, plus a few learning exercises along the way.

## Scripts

### `emailer.py`
Command-line email sender. Takes a recipient, subject, and message body and sends an email via Gmail SMTP (`smtplib`).

```bash
python3 emailer.py recipient@example.com "Subject line" "Message body"
```

Requires a Gmail account with 2-Step Verification and an [App Password](https://myaccount.google.com/apppasswords) — set as an environment variable (see Setup below), not hardcoded in the script.

### `read_emails_CSV.py`
Analyzes exported Brevo email relay logs (CSV) and reports delivery health — sent/delivered/error rates, top error sources by sender and recipient domain, and daily error trends.

```bash
python3 read_emails_CSV.py path/to/export.csv
```

Built after using it to diagnose a real delivery issue on Sevva's mail relay (a misconfigured WordPress site sending to a typo'd domain).

### `rspamd_report.py`
Pulls recent spam-filtering activity from Rspamd's controller API and reports on it — action breakdown, score distribution, top senders getting rejected, which detection rules are firing, and repeat offenders.

```bash
export RSPAMD_PASSWORD="your_rspamd_controller_password"
python3 rspamd_report.py
```

What it reports:
- **Overview** — total messages, action breakdown (no action / reject / soft reject / add header), score distribution
- **Top senders by action** — which senders are getting rejected most
- **Top symbols** — which Rspamd detection rules are firing most often on rejected mail (e.g. `RBL_SPAMHAUS_CSS`, `VIOLATED_DIRECT_SPF`) — usually the most useful part, since it tells you *why* mail is being rejected, not just that it was
- **Repeat offenders** — senders with 3+ rejects in the current snapshot, worth investigating individually

**A real limitation worth knowing:** Rspamd's `/history` endpoint only returns a fixed number of recent messages (`history_rows` in its config — 200 by default), not a long-term log. It's a rolling window — as new mail comes in, older entries fall out. Running this script twice in a row can show slightly different numbers even with no real change in mail health, just because the window shifted.

For real historical analysis beyond that window, the raw log at `/var/log/rspamd/rspamd.log` (plus rotated `.gz` files, governed by `/etc/logrotate.d/rspamd`) is the actual source of longer-term data — but it needs log parsing, not a clean API call, and retention there depends on the `rotate` setting in logrotate.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Don't commit credentials or data exports. This repo's `.gitignore` excludes `*.csv` and should exclude any file containing API keys, tokens, or passwords. Use environment variables or a gitignored `.env` file for secrets instead of hardcoding them.

## Notes

These are personal tools, built incrementally while learning Python — not polished packages. Error handling and structure improve as the scripts get reused, not necessarily on the first version.