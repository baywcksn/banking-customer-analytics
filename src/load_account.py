import pandas as pd
import psycopg

CSV_PATH = "BankingDigitalTwin/output/account.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "banking_analytics",
    "user": "banking_user",
    "password": "banking_password",
}

COLUMNS = [
    "account_id",
    "customer_id",
    "product_id",
    "account_type",
    "status",
    "opened_date",
    "currency",
    "current_balance",
    "overdraft_limit",
    "interest_rate",
]

INSERT_SQL = """
    INSERT INTO account (
        account_id,
        customer_id,
        product_id,
        account_type,
        status,
        opened_date,
        currency,
        current_balance,
        overdraft_limit,
        interest_rate
    )
    VALUES (
        %(account_id)s,
        %(customer_id)s,
        %(product_id)s,
        %(account_type)s,
        %(status)s,
        %(opened_date)s,
        %(currency)s,
        %(current_balance)s,
        %(overdraft_limit)s,
        %(interest_rate)s
    )
    ON CONFLICT (account_id) DO NOTHING;
"""


def main():
    print("Reading account.csv...")

    df = pd.read_csv(
        CSV_PATH,
        usecols=COLUMNS,
        parse_dates=["opened_date"],
    )

    records = df.to_dict("records")

    print(f"Rows loaded from CSV: {len(records)}")

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, records)

        conn.commit()

    print("Account data loaded successfully.")


if __name__ == "__main__":
    main()