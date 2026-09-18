import pandas as pd
import psycopg

CSV_PATH = "BankingDigitalTwin/output/customer.csv"

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "banking_analytics",
    "user": "banking_user",
    "password": "banking_password",
}

COLUMNS = [
    "customer_id",
    "status",
    "segment",
    "lifecycle_stage",
    "financial_literacy_score",
    "risk_appetite",
    "technology_adoption",
    "credit_score",
    "onboarding_date",
]

INSERT_SQL = """
    INSERT INTO customer (
        customer_id,
        status,
        segment,
        lifecycle_stage,
        financial_literacy_score,
        risk_appetite,
        technology_adoption,
        credit_score,
        onboarding_date
    )
    VALUES (
        %(customer_id)s,
        %(status)s,
        %(segment)s,
        %(lifecycle_stage)s,
        %(financial_literacy_score)s,
        %(risk_appetite)s,
        %(technology_adoption)s,
        %(credit_score)s,
        %(onboarding_date)s
    )
    ON CONFLICT (customer_id) DO NOTHING;
"""


def main():
    print("Reading customer.csv...")

    df = pd.read_csv(
        CSV_PATH,
        usecols=COLUMNS,
        parse_dates=["onboarding_date"],
    )

    records = df.to_dict("records")

    print(f"Rows loaded from CSV: {len(records)}")

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, records)

        conn.commit()

    print("Customer data loaded successfully.")


if __name__ == "__main__":
    main()