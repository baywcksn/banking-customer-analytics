import pandas as pd
import psycopg

CSV_PATH = "BankingDigitalTwin/output/account_balance_history.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "banking_analytics",
    "user": "banking_user",
    "password": "banking_password",
}

COLUMNS = [
    "history_id",
    "account_id",
    "balance_date",
    "opening_balance",
    "closing_balance",
    "min_balance",
    "max_balance",
]

INSERT_SQL = """
    INSERT INTO account_balance_history (
        history_id,
        account_id,
        balance_date,
        opening_balance,
        closing_balance,
        min_balance,
        max_balance
    )
    VALUES (
        %(history_id)s,
        %(account_id)s,
        %(balance_date)s,
        %(opening_balance)s,
        %(closing_balance)s,
        %(min_balance)s,
        %(max_balance)s
    )
    ON CONFLICT (history_id) DO NOTHING;
"""


def main():
    print("Reading account_balance_history.csv...")

    total_loaded = 0

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for chunk in pd.read_csv(
                CSV_PATH,
                usecols=COLUMNS,
                chunksize=50_000,
                parse_dates=["balance_date"],
            ):
                records = (
                    chunk.astype(object)
                    .where(pd.notna(chunk), None)
                    .to_dict("records")
                )

                cur.executemany(INSERT_SQL, records)

                conn.commit()

                total_loaded += len(records)

                print(f"Loaded: {total_loaded:,} rows")

    print("Account balance history data loaded successfully.")


if __name__ == "__main__":
    main()