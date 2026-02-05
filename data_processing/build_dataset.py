from data_processing.loaders import (
    load_orders,
    load_sports,
    load_customer_orders
)
from data_processing.aggregations import compute_metrics


def build_dashboard_data():
    orders = load_orders()
    sports = load_sports()
    customer_orders = load_customer_orders()

    return compute_metrics(
        orders=orders,
        sports=sports,
        customer_orders=customer_orders
    )
