import pandas as pd
import psycopg

CSV_PATH = "BankingDigitalTwin/output/transaction.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "banking_analytics",
    "user": "banking_user",
    "password": "banking_password",
}

COLUMNS = [
    "transaction_id",
    "account_id",
    "transaction_type",
    "amount",
    "currency",
    "direction",
    "running_balance",
    "merchant_id",
    "merchant_name",
    "mcc_code",
    "payment_method",
    "channel",
    "transaction_date",
    "transaction_timestamp",
    "enriched_category",
    "is_recurring",
    "status",
]

INSERT_SQL = """
    INSERT INTO transaction (
        transaction_id,
        account_id,
        transaction_type,
        amount,
        currency,
        direction,
        running_balance,
        merchant_id,
        merchant_name,
        mcc_code,
        payment_method,
        channel,
        transaction_date,
        transaction_timestamp,
        enriched_category,
        is_recurring,
        status
    )
    VALUES (
        %(transaction_id)s,
        %(account_id)s,
        %(transaction_type)s,
        %(amount)s,
        %(currency)s,
        %(direction)s,
        %(running_balance)s,
        %(merchant_id)s,
        %(merchant_name)s,
        %(mcc_code)s,
        %(payment_method)s,
        %(channel)s,
        %(transaction_date)s,
        %(transaction_timestamp)s,
        %(enriched_category)s,
        %(is_recurring)s,
        %(status)s
    )
    ON CONFLICT (transaction_id) DO NOTHING;
"""


def main():
    print("Reading transaction.csv...")

    total_loaded = 0

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for chunk in pd.read_csv(
                CSV_PATH,
                usecols=COLUMNS,
                chunksize=50_000,
                parse_dates=[
                    "transaction_date",
                    "transaction_timestamp",
                ],
            ):
                # Convert mcc_code to nullable integer.
                # Missing values become None/SQL NULL.
                chunk["mcc_code"] = chunk["mcc_code"].astype("Int64")

                # Convert pandas missing values (NaN/pd.NA)
                # to Python None so PostgreSQL receives NULL.
                records = (
                    chunk.astype(object)
                    .where(pd.notna(chunk), None)
                    .to_dict("records")
                )

                cur.executemany(INSERT_SQL, records)

                conn.commit()

                total_loaded += len(records)

                print(f"Loaded: {total_loaded:,} rows")

    print("Transaction data loaded successfully.")


if __name__ == "__main__":
    main()