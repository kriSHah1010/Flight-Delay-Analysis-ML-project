import streamlit as st
import pandas as pd
from data_loader import load_featured_data

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

st.title("🤖 ML Delay Predictor")

df = load_featured_data()

st.success("ML predictor page loaded")

ml_df = df.dropna(subset=["AIRLINE", "ORIGIN", "DEST", "month", "day_of_week", "is_weekend", "delay_flag"])
ml_df = ml_df.sample(min(200000, len(ml_df)), random_state=42)

X = ml_df[["AIRLINE", "ORIGIN", "DEST", "month", "day_of_week", "is_weekend"]]
y = ml_df["delay_flag"]

cat_features = ["AIRLINE", "ORIGIN", "DEST"]
num_features = ["month", "day_of_week", "is_weekend"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
        ("num", SimpleImputer(strategy="most_frequent"), num_features),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

with st.spinner("Training model..."):
    model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

st.metric("Model Accuracy", f"{acc * 100:.2f}%")

with st.expander("Classification report"):
    st.text(classification_report(y_test, y_pred))

st.subheader("Try a Prediction")

airlines = sorted(df["AIRLINE"].dropna().unique().tolist())
airports = sorted(df["ORIGIN"].dropna().unique().tolist())
destinations = sorted(df["DEST"].dropna().unique().tolist())

pred_airline = st.selectbox("Airline", airlines)
pred_origin = st.selectbox("Origin", airports)
pred_dest = st.selectbox("Destination", destinations)
pred_month = st.selectbox("Month", list(range(1, 13)))
pred_dow = st.selectbox("Day of week (0=Mon, 6=Sun)", list(range(7)))
pred_weekend = 1 if pred_dow in [5, 6] else 0

if st.button("Predict Delay"):
    input_df = pd.DataFrame([{
        "AIRLINE": pred_airline,
        "ORIGIN": pred_origin,
        "DEST": pred_dest,
        "month": pred_month,
        "day_of_week": pred_dow,
        "is_weekend": pred_weekend
    }])

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    if pred == 1:
        st.error(f"Likely delayed. Delay probability: {prob:.2%}")
    else:
        st.success(f"Likely on time. Delay probability: {prob:.2%}")