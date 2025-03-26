import pandas as pd
import streamlit as st
import openai  # For LLM interaction

# Streamlit UI

st.sidebar.title("Data Profiling Menu")


# Add options to the sidebar (e.g., navigation, user inputs)
selected_option = st.sidebar.selectbox(
    "Choose an option:",
    ["Home", "DefineRules"]
)
 
# Display the selected option's content
if selected_option == "Home":
   st.title("Data Profiling Engine")
   uploaded_file = st.file_uploader("Upload your CSV file for profiling", type=["csv"])
   if uploaded_file:
    # Load the dataset
    data = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.dataframe(data)
    print(data.head())
    data["Transaction Date"] = pd.to_datetime(data["Transaction Date"], errors="coerce")
    # Allow the user to define verification rules
    st.write("### Define Data Verification Rules")
    days_limit = 365
    current_date = pd.Timestamp("today")
    date_365_days_ago = pd.Timestamp("today") - pd.Timedelta(days=365)
    rules = {
    "Transaction Amount should always match with Reported Amount": "Transaction_Amount == Reported_Amount",
    "Amount Balance should be never negative": "Amount_Balance < 0",
    "Transaction Date should not be of future": "`Transaction Date` <= @current_date",
    "Transaction older than 365 days should be flagged": "`Transaction Date` <= @date_365_days_ago",
    "High risk transaction amount > 5000 should be flagged": "Transaction_Amount > 5000"
          }
# Results dictionary
    results = {} 
    # Evaluate the rule
    if st.button("Verify Data"):
        for rule_name, condition in rules.items():
            try:
                results[rule_name] = data.eval(condition, engine="python")
            except Exception as e:
                results[rule_name] = f"Error in rule '{rule_name}': {e}"
            st.write("Verification Result:")
            st.write("RuleName :" ,rule_name)
            #
            data["Violated_Rule"] = results[rule_name]
            st.dataframe(data[["Customer_ID", "Amount_Balance", "Transaction_Amount", "Reported_Amount", "Transaction Date", "Violated_Rule"]],width=1000)

    # Data-Powered Profiling
    st.write("### Profile Insights Using LLM")
    if st.button("Profile Insights Using LLM"):
        prompt = f"Provide detailed profiling and verification insights for the following data: {data.head().to_csv(index=False)}"
        
        # OpenAI API (replace with your key)
        openai.api_key = ""
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        st.text_area("Profiling Insights", response.choices[0].text.strip())


elif selected_option == "DefineRules":
    st.title("Data Profiling Rules")
    options = ["Transaction Amount should always match with Reported Amount.", 
    "Amount Balance should be never negative.", 
    "Transaction Date should not be of future.", 
    "Transaction older than 365 days should be flagged.",
    "High risk transaction amount > 5000 should be flagged"]
    selected_items = st.multiselect("Select items from the list:", options)

# Button
    if st.button("Show Selected Items"):
     if selected_items:
        st.write("You selected:", selected_items)
     else:
        st.write("No items selected.")

# Upload CSV file


