import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Wczytanie danych
@st.cache_data
def load_dashboard_data():
    return pd.read_pickle("data/transaction_data.pkl")

data = load_dashboard_data()
# order_values = data["order_values"]

st.title("Transakcje")

# =========================
# Informacja o ekstremalnych zamówieniach
st.subheader("Największe zamówienia")
top_orders = data["top_orders"]
# jeśli mamy też order_id, można to zrobić lepiej z join z orders_df
st.dataframe(top_orders)


st.markdown("""
> Uwaga: Ze względu na duże różnice wartości zamówień, histogramy są podzielone na dwa zakresy, aby lepiej zobaczyć rozkład.
""")

# =========================
# Histogram 1: 0 - 900 zł
# low_values = order_values[order_values <= 900]
# =========================
# Histogram 0-900 zł
hist_low = data["hist_low"]
hist_low["bin_start_rounded"] = hist_low["bin_start"].round(1)
hist_low["bin_end_rounded"] = hist_low["bin_end"].round(1)

fig_low = px.bar(
    hist_low,
    x="bin_mid",
    y="count",
    text="count",
    labels={"bin_mid": "Środek przedziału [zł]", "count": "Liczba zamówień"},
    hover_data={
        "bin_start_rounded": True,
        "bin_end_rounded": True,
        "count": True,
        "bin_mid": False
    },
    width=1000,
    height=600
)

fig_low.update_traces(
    hovertemplate="Zakres: %{customdata[0]} – %{customdata[1]} zł<br>Liczba zamówień: %{y}",
    marker_color="steelblue",  # jednolity kolor
    hoverlabel=dict(
        font_size=16,  # rozmiar czcionki w tooltipie
        font_family="Arial"
    )
)

fig_low.update_layout(
    title="Histogram wartości zamówień (0–900 zł)",
    title_font_size=22,
    xaxis=dict(
        title="Wartość zamówienia [zł]",
        title_font=dict(size=16, family="Arial", color="white"),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title="Liczba zamówień",
        title_font=dict(size=16, family="Arial", color="white"),
        tickfont=dict(size=14)
    ),
    margin=dict(l=80, r=50, t=80, b=80)  # zwiększamy marginesy, żeby tytuły osi się zmieściły
)
st.plotly_chart(fig_low, use_container_width=True)

# =========================
# Histogram 900-80 000 zł
hist_high = data["hist_high"]
hist_high["bin_start_rounded"] = hist_high["bin_start"].round(1)
hist_high["bin_end_rounded"] = hist_high["bin_end"].round(1)

fig_high = px.bar(
    hist_high,
    x="bin_mid",
    y="count",
    text="count",
    labels={"bin_mid": "Środek przedziału [zł]", "count": "Liczba zamówień"},
    hover_data={
        "bin_start_rounded": True,
        "bin_end_rounded": True,
        "count": True,
        "bin_mid": False
    },
    width=1000,
    height=600
)

fig_high.update_traces(
    hovertemplate="Zakres: %{customdata[0]} – %{customdata[1]} zł<br>Liczba zamówień: %{y}",
    marker_color="steelblue",  # jednolity kolor
    hoverlabel=dict(
        font_size=16,  # rozmiar czcionki w tooltipie
        font_family="Arial"
    )
)
fig_high.update_layout(
    title="Histogram wartości zamówień (900–80 000 zł)",
    title_font_size=22,
    xaxis=dict(
        title="Wartość zamówienia [zł]",
        title_font=dict(size=16, family="Arial", color="white"),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title="Liczba zamówień",
        title_font=dict(size=16, family="Arial", color="white"),
        tickfont=dict(size=14)
    ),
    margin=dict(l=80, r=50, t=80, b=80)  # zwiększamy marginesy, żeby tytuły osi się zmieściły
)
st.plotly_chart(fig_high, use_container_width=True)
st.markdown("---")  # separator

# =========================
# Sekcja 2: Liczba zamówień na klienta
st.header("Liczba zamówień dokonanych przez klientów")

order_counts = data['orders_per_customer']

fig_orders = px.bar(
    order_counts,
    x="number_of_orders",
    y="number_of_customers",
    title="Rozkład liczby zamówień na klienta",
    labels={"number_of_orders": "Liczba zamówień", "number_of_customers": "Liczba klientów"},
    text="number_of_customers"
)
fig_orders.update_traces(textposition='outside')  # liczba klientów nad słupkami
st.plotly_chart(fig_orders, use_container_width=True)
