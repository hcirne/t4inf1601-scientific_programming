import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# Page configuration
# ---------------------------
st.set_page_config(
    page_title="Laptop Price Guide",
    page_icon="💻",
    layout="wide"
)

# Load saved model and metadata
# ---------------------------
model = joblib.load("models/laptop_price_model.pkl")
meta = joblib.load("models/app_metadata.pkl")
data = pd.read_csv("data/laptops_cleaned.csv")

# Title and intro
# ---------------------------
st.title("💻 Laptop Price Guide")
st.write("Predict a laptop's fair price based on its specifications.")

st.markdown("---")

# Two-column layout
# ---------------------------
left_col, right_col = st.columns([1, 1])

# User inputs
# ---------------------------
with left_col:
    st.subheader("Enter Laptop Specifications")

    brand = st.selectbox("Brand", meta["brands"])

    brand_filtered = data[data["brand"] == brand]

    cpu_options = sorted(brand_filtered["cpu"].dropna().unique().tolist())
    cpu = st.selectbox("CPU", cpu_options)

    cpu_filtered = brand_filtered[brand_filtered["cpu"] == cpu]

    storage_type_options = sorted(cpu_filtered["storage_type"].dropna().unique().tolist())
    if not storage_type_options:
        storage_type_options = meta["storage_types"]
    storage_type = st.selectbox("Storage Type", storage_type_options)

    gpu_options = sorted(cpu_filtered["gpu"].dropna().unique().tolist())
    if not gpu_options:
        gpu_options = meta["gpus"]
    gpu = st.selectbox("GPU", gpu_options)

    touch_options = sorted(cpu_filtered["touch"].dropna().unique().tolist())
    if not touch_options:
        touch_options = meta["touch_options"]
    touch = st.selectbox("Touch Screen", touch_options)

    status_options = sorted(cpu_filtered["status"].dropna().unique().tolist())
    if not status_options:
        status_options = meta["status_options"]
    status = st.selectbox("Condition", status_options)

    ram = st.slider("RAM (GB)", min_value=4, max_value=64, value=16, step=4)
    storage = st.slider("Storage (GB)", min_value=128, max_value=2048, value=512, step=128)
    screen = st.slider("Screen Size (inches)", min_value=10.0, max_value=18.0, value=15.6, step=0.1)

    st.markdown("### Optional Deal Check")
    listing_price = st.number_input(
        "Seller's Asking Price ($)",
        min_value=0.0,
        value=1000.0,
        step=50.0
    )

# Prediction section
# ---------------------------
with right_col:
    st.subheader("Prediction Result")

    input_df = pd.DataFrame([{
        "brand": brand,
        "cpu": cpu,
        "ram": ram,
        "storage": storage,
        "storage_type": storage_type,
        "gpu": gpu,
        "screen": screen,
        "touch": touch,
        "status": status
    }])

    predicted_price = float(model.predict(input_df)[0])
    price_difference = listing_price - predicted_price

    st.metric("Predicted Fair Price", f"${predicted_price:,.2f}")

    # Determine verdict
    if predicted_price == 0:
        pct_diff = 0
    else:
        pct_diff = price_difference / predicted_price

    if pct_diff <= -0.10:
        verdict = "Good Deal"
    elif pct_diff < 0.10:
        verdict = "Fairly Priced"
    else:
        verdict = "Overpriced"

    st.metric("Verdict", verdict)
    st.metric("Listing Price Minus Predicted Price", f"${price_difference:,.2f}")

    # Gauge chart
    gauge_max = max(meta["price_max"], predicted_price * 1.1)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=predicted_price,
            title={"text": "Predicted Price Tier"},
            gauge={
                "axis": {"range": [meta["price_min"], gauge_max]},
                "steps": [
                    {"range": [meta["price_min"], meta["price_q33"]], "color": "lightgreen"},
                    {"range": [meta["price_q33"], meta["price_q66"]], "color": "gold"},
                    {"range": [meta["price_q66"], gauge_max], "color": "salmon"}
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": predicted_price
                }
            }
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Price Band Guide")
    st.write(
        f"Budget: up to ${meta['price_q33']:,.0f}"
    )
    st.write(
        f"Mid-Range: ${meta['price_q33']:,.0f} to ${meta['price_q66']:,.0f}"
    )
    st.write(
        f"Premium: above ${meta['price_q66']:,.0f}"
    )

# Explanation section
# ---------------------------
st.markdown("---")
st.subheader("How This App Works")
st.write(
    "This app uses a machine learning regression model trained on laptop features "
    "such as brand, CPU, RAM, storage, GPU, screen size, touch capability, and condition "
    "to estimate a fair market price."
)