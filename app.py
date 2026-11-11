
import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from preprocess import preprocess_user_input

# Load model
model = joblib.load('saved_model/model.pkl')

st.set_page_config(page_title="Explorer PM – Insurance & Investment", page_icon="💼", layout="wide")

st.title("🧠 Explorer PM – AI Personal Finance Assistant")
st.markdown("### Empowering you with insights on **Insurance Premiums**, **Investments**, and **Risk Gaps**.")

tabs = st.tabs(["💸 Insurance Premium Prediction", "💼 Investment Suggestion", "🛡️ Risk & Insurance Gap Report"])

# 💸 Insurance Premium Tab
with tabs[0]:
    st.subheader("💸 Predict Your Monthly Insurance Premium")
    with st.form("premium_form"):
        user_input = {
            'Age': st.slider("Age", 18, 100, 30),
            'Occupation': st.selectbox("Occupation", ['Retired', 'Salaried', 'Student', 'Self-Employed']),
            'Assets': st.number_input("Assets", value=5000000),
            'Investments': st.number_input("Investments", value=100000),
            'Savings': st.number_input("Savings", value=50000),
            'Debt': st.number_input("Debt", value=20000),
            'Gross monthly income': st.number_input("Gross Monthly Income", value=50000),
            'Net monthly income': st.number_input("Net Monthly Income", value=40000),
            'Rent/Mortgage': st.number_input("Rent/Mortgage", value=2000),
            'Utilities': st.number_input("Utilities", value=500),
            'Car Payment': st.number_input("Car Payment", value=2000),
            'Debt Payments': st.number_input("Debt Payments", value=1000),
            'Groceries': st.number_input("Groceries", value=3000),
            'Clothes': st.number_input("Clothes", value=500),
            'Phone': st.number_input("Phone", value=100),
            'Subscriptions': st.number_input("Subscriptions", value=50),
            'Miscellaneous': st.number_input("Miscellaneous", value=200),
            'Vacations': st.number_input("Vacations", value=1000),
            'Gifts': st.number_input("Gifts", value=300),
            'Emergency Fund': st.number_input("Emergency Fund", value=10000),
            'Dining out': st.number_input("Dining Out", value=200),
            'Movies': st.number_input("Movies", value=50),
            'Other': st.number_input("Other Expenses", value=100)
        }
        submitted = st.form_submit_button("🔍 Predict Premium")

    if submitted:
        try:
            input_df = preprocess_user_input(user_input, model)
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Estimated Monthly Insurance Premium: ₹{prediction:,.2f}")

            st.markdown("#### 🧾 Expense Breakdown")
            expense_keys = ['Rent/Mortgage', 'Utilities', 'Car Payment', 'Debt Payments', 'Groceries', 'Clothes',
                            'Phone', 'Subscriptions', 'Miscellaneous', 'Vacations', 'Gifts', 'Dining out', 'Movies', 'Other']
            expense_vals = [user_input[key] for key in expense_keys]

            fig, ax = plt.subplots()
            ax.pie(expense_vals, labels=expense_keys, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# 💼 Investment Suggestion Tab
with tabs[1]:
    st.subheader("💼 Smart Investment Suggestions")
    age = st.slider("Your Age", 18, 70, 30)
    risk_profile = st.selectbox("Your Risk Profile", ["Conservative", "Moderate", "Aggressive"])
    monthly_investment = st.number_input("Amount to Invest Monthly", value=5000)

    if st.button("📈 Show Plan"):
        if risk_profile == "Conservative":
            st.info(f"✅ Suggested:\n- ₹{monthly_investment*0.6:.0f} in FD\n- ₹{monthly_investment*0.4:.0f} in PPF")
        elif risk_profile == "Moderate":
            st.info(f"✅ Suggested:\n- ₹{monthly_investment*0.6:.0f} in SIP\n- ₹{monthly_investment*0.4:.0f} in ELSS")
        else:
            st.info(f"✅ Suggested:\n- ₹{monthly_investment*0.7:.0f} in Equity MF\n- ₹{monthly_investment*0.3:.0f} in Crypto/REITs")

# 🛡️ Risk Gap Tab
with tabs[2]:
    st.subheader("🛡️ Risk & Insurance Gap Analysis")
    current_life_cover = st.number_input("Current Life Cover (₹)", value=1000000)
    current_health_cover = st.number_input("Current Health Cover (₹)", value=300000)
    dependents = st.slider("Dependents", 0, 5, 2)
    annual_income = st.number_input("Annual Income (₹)", value=600000)

    if st.button("📊 Analyze Insurance Gap"):
        ideal_life = annual_income * 10 + dependents * 500000
        ideal_health = 1000000 + dependents * 200000

        st.write(f"📌 Recommended Life Cover: ₹{ideal_life:,.0f}")
        st.write(f"📌 Recommended Health Cover: ₹{ideal_health:,.0f}")

        if current_life_cover < ideal_life:
            st.warning(f"⚠️ Gap in Life Cover: ₹{ideal_life - current_life_cover:,.0f}")
        else:
            st.success("✅ Life Insurance is Sufficient")

        if current_health_cover < ideal_health:
            st.warning(f"⚠️ Gap in Health Cover: ₹{ideal_health - current_health_cover:,.0f}")
        else:
            st.success("✅ Health Insurance is Sufficient")
