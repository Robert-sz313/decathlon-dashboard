import pandas as pd
from data_processing.loaders import load_orders, load_customer_orders
import numpy as np

def build_and_save_transaction_data():
    # --- wczytanie danych ---
    orders = load_orders()
    customer_orders = load_customer_orders()

    # --- statystyki wartości zamówień ---
    avg_value = orders["value"].mean()
    median_value = orders["value"].median()
    min_value = orders["value"].min()
    max_value = orders["value"].max()

    # --- histogram kwot transakcji ---
    # hist_values = orders["value"]

    # --- liczba zamówień na klienta ---
    orders_per_customer = customer_orders.groupby("customer_id")["order_id"].nunique()
    order_counts = orders_per_customer.value_counts().sort_index()  # np. 1 transakcja -> ilu klientów, 2 transakcje -> ilu itd.
    order_counts = order_counts.reset_index()
    order_counts.columns = ["number_of_orders", "number_of_customers"]
    order_values = orders["value"]

    top_orders = orders.sort_values("value", ascending=False).head(5)
    # dołączamy customer_id
    top_orders = top_orders.merge(customer_orders, on="order_id", how="left")[["order_id", "customer_id", "value"]]

    # Histogram 0-900 zł
    low_values = order_values[order_values <= 900]
    counts_low, bins_low = np.histogram(low_values, bins=30)

    hist_low = pd.DataFrame({
        "bin_start": bins_low[:-1],
        "bin_end": bins_low[1:],
        "bin_mid": (bins_low[:-1] + bins_low[1:]) / 2,  # <--- środek przedziału
        "count": counts_low
    })

    # Histogram 900-80 000 zł
    high_values = order_values[(order_values > 900) & (order_values <= 80000)]
    counts_high, bins_high = np.histogram(high_values, bins=40)

    hist_high = pd.DataFrame({
        "bin_start": bins_high[:-1],
        "bin_end": bins_high[1:],
        "bin_mid": (bins_high[:-1] + bins_high[1:]) / 2,  # <--- środek przedziału
        "count": counts_high
    })
    # --- zapis do pliku pickle ---
    pd.to_pickle({
        "summary": {
            "avg_order_value": avg_value,
            "median_order_value": median_value,
            "min_order_value": min_value,
            "max_order_value": max_value
        },
        "top_orders": top_orders,
        "hist_low": hist_low,
        "hist_high": hist_high,
        # "order_values": hist_values,
        "orders_per_customer": order_counts
    }, "data/transaction_data.pkl")

    print("Transaction data saved!")

# Wywołanie funkcji
build_and_save_transaction_data()
