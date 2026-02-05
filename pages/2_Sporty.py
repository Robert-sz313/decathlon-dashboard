import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_sport_data():
    return pd.read_pickle("data/sport_page_data.pkl")

data = load_sport_data()
sport_counts = data["sport_counts"]

st.set_page_config(
    page_title="Sporty Decathlon",
    page_icon=":soccer:",
    layout="wide"
)

st.title("Sporty klientów Decathlon")

# Najpopularniejszy i najmniej popularny sport
st.info(f"**Najpopularniejszy sport:** {data['most_popular']}")
st.info(f"**Najmniej popularny sport:** {data['least_popular']}")

# --- wykres słupkowy ---
st.subheader("Liczba osób uprawiających poszczególne sporty")
fig_bar = px.bar(
    sport_counts,
    x="sport",
    y="count",
    labels={"sport": "Sport", "count": "Liczba osób"},
    color="count",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- wykres kołowy ---
st.subheader("Udział procentowy klientów według dyscypliny")
fig_pie = px.pie(
    sport_counts,
    names="sport",
    values="pct",
    title="Procent klientów uprawiających dany sport",
    width=800,  # szerokość w pikselach
    height=600  # wysokość w pikselach
)
fig_pie.update_traces(
    hovertemplate="%{label}<extra></extra>",  # tylko nazwa dyscypliny
    hoverlabel=dict(
        font_size=18,      # rozmiar czcionki w tooltipie
        font_family="Arial" # opcjonalnie zmiana fontu
    )
)
st.plotly_chart(fig_pie, use_container_width=True)
