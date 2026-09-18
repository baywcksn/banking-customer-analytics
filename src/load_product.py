import pandas as pd
import psycopg

CSV_PATH = "BankingDigitalTwin/output/product.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "banking_analytics",
    "user": "banking_user",
    "password": "banking_password",
}

COLUMNS = [
    "product_id",
    "product_code",
    "name",
    "category",
    "status",
    "launch_date",
    "currency",
    "fee_monthly",
    "rate_min",
    "rate_max",
]

INSERT_SQL = """
    INSERT INTO product (
        product_id,
        product_code,
        name,
        category,
        status,
        launch_date,
        currency,
        fee_monthly,
        rate_min,
        rate_max
    )
    VALUES (
        %(product_id)s,
        %(product_code)s,
        %(name)s,
        %(category)s,
        %(status)s,
        %(launch_date)s,
        %(currency)s,
        %(fee_monthly)s,
        %(rate_min)s,
        %(rate_max)s
    )
    ON CONFLICT (product_id) DO NOTHING;
"""


def main():
    print("Reading product.csv...")

    df = pd.read_csv(
        CSV_PATH,
        usecols=COLUMNS,
        parse_dates=["launch_date"],
    )

    records = df.to_dict("records")

    print(f"Rows loaded from CSV: {len(records)}")

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, records)

        conn.commit()

    print("Product data loaded successfully.")


if __name__ == "__main__":
    main()