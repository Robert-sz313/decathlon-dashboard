import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Dashboard Decathlon",  # tytuł w zakładce przeglądarki
    page_icon=":bar_chart:",           # możesz dodać emoji lub ikonę
    layout="wide",                     # szeroki layout
)
@st.cache_data
def load_dashboard_data():
    return pd.read_pickle("data/dashboard_data.pkl")

data = load_dashboard_data()

st.title("Decathlon Dashboard")

# =========================
# KPI w dwóch kolumnach
col1, col2, col3= st.columns(3)

col1.metric("Średnia wartość zamówienia", f"{data['summary']['avg_order_value']:.2f} zł")
col1.metric("Mediana wartości zamówienia", f"{data['summary']['median_order_value']:.2f} zł")

col2.metric("Odsetek klientów z 2 i więcej zamówieniami", f"{data['summary']['multi_order_customers_pct']:.2f}%")
col2.metric("Odsetek klientów z 3 i więcej sportami", f"{data['summary']['multi_sport_customers_pct']:.2f}%")

# --- kolumna 3: najpopularniejsze sporty ---
most_sport = data["most_popular_sport"]
least_sport = data["least_popular_sport"]

col3.metric("Najpopularniejszy sport", f"{most_sport['sport']} - {most_sport['count']} osób")
col3.metric("Najmniej popularny sport", f"{least_sport['sport']} - {least_sport['count']} osób")

# =========================
st.markdown("---")  # separator

# Sekcja O mnie
st.header("O mnie")
st.markdown("""
**Robert Szymko**  
Email: rszymko@gmail.com  
Tel: 691037660  
Rola: Data Analyst / Candidate  
Technologie: Python, Streamlit, Plotly
LinkedIn: [linkedin.com/in/robert-szymko](https://www.linkedin.com/in/robert-szymko-56b382278/)  
""")
