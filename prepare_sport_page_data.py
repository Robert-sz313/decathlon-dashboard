import pandas as pd
from data_processing.loaders import load_sports


def build_and_save_sport_page_data():
    # --- wczytanie danych ---
    sports = load_sports()

    # --- agregacje ---
    total_customers = sports["customer_id"].nunique()

    # Liczba osób uprawiających każdy sport
    sport_counts = sports["sport"].value_counts().reset_index()
    sport_counts.columns = ["sport", "count"]

    # Procent klientów uprawiających każdy sport
    sport_counts["pct"] = sport_counts["count"] / total_customers * 100

    # Najpopularniejszy i najmniej popularny sport
    most_popular = sport_counts.iloc[0]["sport"]
    least_popular = sport_counts.iloc[-1]["sport"]

    # --- zapis do pickle ---
    pd.to_pickle({
        "sport_counts": sport_counts,
        "most_popular": most_popular,
        "least_popular": least_popular
    }, "data/sport_page_data.pkl")

    print("Sport page data saved!")


if __name__ == "__main__":
    build_and_save_sport_page_data()
