import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        .hero {
            background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%);
            padding: 24px 28px;
            border-radius: 22px;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
            margin-bottom: 18px;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
            color: white;
        }

        .hero p {
            margin-top: 8px;
            opacity: 0.92;
            font-size: 1rem;
            color: white;
        }

        .section-card {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 18px;
            padding: 18px 18px 10px 18px;
            margin-top: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.04);
            color: var(--text-color);
        }

        .section-card * {
            color: var(--text-color);
        }

        .insight-box {
            background: rgba(14, 165, 233, 0.10);
            border-left: 6px solid #0ea5e9;
            padding: 14px 16px;
            border-radius: 14px;
            margin-top: 10px;
            color: var(--text-color);
        }

        .insight-box * {
            color: var(--text-color);
        }

        .small-label {
            font-size: 0.85rem;
            color: var(--text-color);
            opacity: 0.75;
            margin-bottom: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )