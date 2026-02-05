import pandas as pd
import time
import streamlit as st

# =========================
# 1. Wczytywanie sports.csv
# =========================
# @st.cache_data
def load_sports(path="data/sports.csv"):
    df = pd.read_csv(path)

    # typy
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")

    # usuwamy niekompletne dane
    df = df.dropna(subset=["customer_id", "sport"])

    # rzutowanie po dropna
    df["customer_id"] = df["customer_id"].astype(int)

    df = df.drop_duplicates()
    # unique_sports = df["sport"].unique()
    # print(f"Liczba unikatowych sportów: {len(unique_sports)}")
    # print(unique_sports)

    return df

# =========================
# 2. Wczytywanie customer_orders.csv
# =========================
# @st.cache_data
def load_customer_orders(path="data/customer_orders.csv"):
    df = pd.read_csv(path)
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df = df.dropna(subset=["customer_id", "order_id"])
    df["customer_id"] = df["customer_id"].astype(int)
    df["order_id"] = df["order_id"].astype(int)


    df = df.drop_duplicates()
    return df

# =========================
# 3. Wczytywanie orders.csv
# =========================
# @st.cache_data
def load_orders(path="data/orders.csv"):
    df = pd.read_csv(path)

    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["products"] = pd.to_numeric(df["products"], errors="coerce")

    df = df.dropna(subset=["order_id", "value", "products"])

    df["order_id"] = df["order_id"].astype(int)
    df["products"] = df["products"].astype(int)

    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["order_id"])

    # invalid_rows = df[(df["value"] <= 0) | (df["products"] <= 0)]
    # print(f"Liczba wierszy z value <= 0 lub products <= 0: {len(invalid_rows)}")
    # print("Niepoprawne wiersze:")
    # print(invalid_rows)

    df = df[(df["value"] > 0) & (df["products"] > 0)]

    return df

# =========================
# Przykład użycia
# =========================
if __name__ == "__main__":
    start = time.time()

    sports_df = load_sports()
    customer_orders_df = load_customer_orders()
    orders_df = load_orders()

    end = time.time()

    print(f"Czas wykonania funkcji: {end - start:.4f} sekund")