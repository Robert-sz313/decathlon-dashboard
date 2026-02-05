import pandas as pd
from data_processing.loaders import load_orders, load_sports, load_customer_orders

def build_and_save_dashboard_data():
    # --- wczytywanie danych ---
    orders = load_orders()
    sports = load_sports()
    customer_orders = load_customer_orders()

    # --- statystyki i agregacje ---
    avg_value = orders["value"].mean()
    median_value = orders["value"].median()
    mode_value = orders["value"].round(0).mode().iloc[0]

    orders_per_customer = customer_orders.groupby("customer_id")["order_id"].nunique()
    multi_order_pct = (orders_per_customer > 1).mean() * 100

    sports_per_customer = sports.groupby("customer_id")["sport"].nunique()
    multi_sport_pct = (sports_per_customer > 1).mean() * 100

    sport_counts = sports["sport"].value_counts().reset_index()
    sport_counts.columns = ["sport", "count"]

    # --- Najbardziej i najmniej popularny sport ---
    most_popular_sport = sport_counts.sort_values("count", ascending=False).iloc[0]
    least_popular_sport = sport_counts.sort_values("count", ascending=True).iloc[0]

    # --- zapis do plików (pickle lub parquet) ---
    pd.to_pickle({
        "summary": {
            "avg_order_value": avg_value,
            "median_order_value": median_value,
            "mode_order_value": mode_value,
            "multi_order_customers_pct": multi_order_pct,
            "multi_sport_customers_pct": multi_sport_pct,
        },
        "sport_counts": sport_counts,
        "most_popular_sport": {
            "sport": most_popular_sport["sport"],
            "count": int(most_popular_sport["count"])
        },
        "least_popular_sport": {
            "sport": least_popular_sport["sport"],
            "count": int(least_popular_sport["count"])
        },
        "order_values": orders["value"],
    }, "data/dashboard_data.pkl")

    print("Dashboard data saved!")

build_and_save_dashboard_data()
