import streamlit as st
import pandas as pd
import plotly.express as px

# Expense file ka naam
EXPENSE_FILE = "expenses.csv"

# Categories aur unki subcategories
categories = {
    "Food": ["Groceries", "Restaurants", "Snacks"],
    "Transport": ["Fuel", "Public Transport", "Taxi"],
    "Utilities": ["Electricity", "Water", "Internet"],
    "Entertainment": ["Movies", "Concerts", "Games"],
    "Health": ["Doctor", "Medicine", "Gym"],
    "Shopping": ["Clothing", "Electronics", "Accessories"],
    "Maintenance": ["Plumbing", "Electrical", "Car Repair"],
    "Beauty & Personal Care": ["Salon", "Makeup", "Skincare"],
    "Outing": ["Picnic", "Tours", "Adventure"]
}

# Expenses ko load karne ka function
def load_expenses():
    try:
        return pd.read_csv(EXPENSE_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Category", "Subcategory", "Amount", "Description"])

# Expenses ko save karne ka function
def save_expense(expense):
    expenses = load_expenses()
    expenses = pd.concat([expenses, pd.DataFrame([expense])], ignore_index=True)
    expenses.to_csv(EXPENSE_FILE, index=False)

# Streamlit App UI
st.title("💰 Expense Tracker App")

# Category selection with dynamic subcategory update
category = st.selectbox("Select Category", list(categories.keys()), key="category")

# Initialize subcategory session state if not present
if "subcategory_options" not in st.session_state:
    st.session_state.subcategory_options = categories[category]

# Update subcategory when category changes
st.session_state.subcategory_options = categories[category]
subcategory = st.selectbox("Select Subcategory", options=st.session_state.subcategory_options, key="subcategory")

# Expense details input
date = st.date_input("Date")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
description = st.text_area("Description")

# Add Expense Button
if st.button("Add Expense"):
    if amount > 0:
        save_expense({"Date": date, "Category": category, "Subcategory": subcategory, "Amount": amount, "Description": description})
        st.success("Expense Added Successfully!")
    else:
        st.error("Amount must be greater than zero!")

# Display stored expenses
expenses = load_expenses()
if not expenses.empty:
    st.subheader("📊 Expense Summary")
    st.dataframe(expenses)

    # Category-wise expense graph
    fig = px.bar(expenses, x="Category", y="Amount", color="Subcategory", barmode="group",
                 title="Category-wise Expenses", labels={"Amount": "Total Spent ($)"})
    st.plotly_chart(fig)
else:
    st.info("No expenses recorded yet.")