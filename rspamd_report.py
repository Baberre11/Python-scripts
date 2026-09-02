import os
import requests
import pandas as pd
from collections import Counter

RSPAMD_URL = "http://100.83.56.35:11334"
PASSWORD = os.environ.get("RSPAMD_PASSWORD")

if not PASSWORD:
    raise SystemExit("RSPAMD_PASSWORD environment variable not set")


def fetch_history():
    response = requests.get(f"{RSPAMD_URL}/history", headers={"Password": PASSWORD})
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data if isinstance(data, list) else data.get('rows', data))


def print_overview(df):
    print(f"Total messages: {len(df)}")
    print()
    print("Action breakdown:")
    print(df['action'].value_counts())
    print()
    print("Score stats:")
    print(df['score'].describe())
    print()


def print_top_senders_by_action(df, action, top_n=10):
    subset = df[df['action'] == action]
    if subset.empty:
        return
    print(f"Top senders with action '{action}':")
    print(subset['sender_smtp'].value_counts().head(top_n))
    print()


def print_top_symbols(df, action=None, top_n=15):
    subset = df[df['action'] == action] if action else df
    label = f"for action '{action}'" if action else "overall"

    symbol_counter = Counter()
    for symbols in subset['symbols']:
        if isinstance(symbols, dict):
            symbol_counter.update(symbols.keys())

    print(f"Top symbols triggered {label}:")
    for symbol, count in symbol_counter.most_common(top_n):
        print(f"  {symbol}: {count}")
    print()


def print_repeat_offenders(df, min_rejects=3):
    rejected = df[df['action'] == 'reject']
    counts = rejected['sender_smtp'].value_counts()
    repeat = counts[counts >= min_rejects]
    if not repeat.empty:
        print(f"Repeat offenders ({min_rejects}+ rejects):")
        print(repeat)
        print()


def main():
    df = fetch_history()
    print_overview(df)
    print_top_senders_by_action(df, 'reject')
    print_top_symbols(df, action='reject')
    print_repeat_offenders(df)


if __name__ == "__main__":
    main()