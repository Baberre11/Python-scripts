import argparse
import pandas as pd


def load_data(filepath):
    df = pd.read_csv(filepath)
    df['ts'] = pd.to_datetime(df['ts'], format='%d-%m-%Y %H:%M:%S')
    return df


def print_overview(df):
    print(f"Total events: {len(df)}")
    print(f"Date range: {df['ts'].min()} to {df['ts'].max()}")
    print()
    print("Event counts:")
    print(df['st_text'].value_counts())
    print()


def print_delivery_health(df):
    total_sent = (df['st_text'] == 'Sent').sum()
    delivered = (df['st_text'] == 'Delivered').sum()
    errors = (df['st_text'] == 'Error').sum()
    soft_bounce = (df['st_text'] == 'Soft bounce').sum()
    hard_bounce = (df['st_text'] == 'Hard bounce').sum()
    blocked = (df['st_text'] == 'Blocked').sum()
    deferred = (df['st_text'] == 'Deferred').sum()

    print("Delivery health:")
    print(f"  Sent:          {total_sent}")
    if total_sent > 0:
        print(f"  Delivered:     {delivered}  ({delivered/total_sent*100:.1f}% of sent)")
        print(f"  Errors:        {errors}  ({errors/total_sent*100:.1f}% of sent)")
    print(f"  Soft bounces:  {soft_bounce}")
    print(f"  Hard bounces:  {hard_bounce}")
    print(f"  Blocked:       {blocked}")
    print(f"  Deferred:      {deferred}")
    print()


def print_top_error_sources(df, top_n=10):
    errors_df = df[df['st_text'] == 'Error']
    print(f"Top {top_n} senders by error count:")
    print(errors_df['frm'].value_counts().head(top_n))
    print()

    print(f"Top {top_n} recipient domains by error count:")
    domains = errors_df['email'].str.split('@').str[1]
    print(domains.value_counts().head(top_n))
    print()


def print_daily_error_trend(df):
    errors_df = df[df['st_text'] == 'Error'].copy()
    errors_df['date'] = errors_df['ts'].dt.date
    print("Errors per day:")
    print(errors_df.groupby('date').size())
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze Brevo email log CSV exports")
    parser.add_argument("filepath", help="Path to the CSV file to analyze")
    args = parser.parse_args()

    df = load_data(args.filepath)

    print_overview(df)
    print_delivery_health(df)
    print_top_error_sources(df)
    print_daily_error_trend(df)


if __name__ == "__main__":
    main()