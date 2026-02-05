def compute_metrics(orders, sports, customer_orders):
    # --- PODSUMOWANIE ---
    avg_value = orders["value"].mean()
    median_value = orders["value"].median()
    mode_value = orders["value"].round(0).mode().iloc[0]

    # klienci z >1 zamówieniem
    orders_per_customer = customer_orders.groupby("customer_id")["order_id"].nunique()
    multi_order_pct = (orders_per_customer > 1).mean() * 100

    # klienci z >1 sportem
    sports_per_customer = sports.groupby("customer_id")["sport"].nunique()
    multi_sport_pct = (sports_per_customer > 1).mean() * 100

    # --- WYKRESY ---
    sport_counts = sports["sport"].value_counts().reset_index()
    sport_counts.columns = ["sport", "count"]

    return {
        "summary": {
            "avg_order_value": avg_value,
            "median_order_value": median_value,
            "mode_order_value": mode_value,
            "multi_order_customers_pct": multi_order_pct,
            "multi_sport_customers_pct": multi_sport_pct,
        },
        "sport_counts": sport_counts,
        "order_values": orders["value"],
    }
