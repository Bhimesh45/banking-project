import pandas as pd
from app.db import get_connection

def detect_fraud():
    conn = get_connection()

    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, conn)

    conn.close()

    # High-value transactions
    high_value = df[df['AMOUNT'] > 50000]

    # Frequent transactions
    freq = df.groupby('ACCOUNT_ID').size().reset_index(name='count')
    frequent_accounts = freq[freq['count'] >= 5]

    return {
        "high_value": high_value.to_dict(orient="records"),
        "frequent_accounts": frequent_accounts.to_dict(orient="records")
    }