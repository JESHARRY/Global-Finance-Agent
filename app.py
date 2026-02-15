import streamlit as st
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from finance_tools import get_exchange_rates, get_stock_index_info, get_hq_location_link

# UI Setup
st.set_page_config(page_title="Fin-Agent", page_icon="🏦")
st.title("🏦 Global Finance intelligence Agent")

# Model and Tools
# Create the model with built-in retry logic
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0).with_retry(
    stop_after_attempt=6,  # Retry up to 6 times
    wait_exponential_jitter=True  # Wait longer between each retry
)
tools = [get_exchange_rates, get_stock_index_info, get_hq_location_link]
prompt = hub.pull("hwchase17/react")

# Agent Initialization
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

user_input = st.text_input("Which country's markets should I analyze?", placeholder="Japan")

if st.button("Generate Report"):
    with st.spinner("Accessing global markets..."):
        # We wrap the user input in the specific lab requirements
        task = f"For {user_input}: Give me official currency, exchange rates to USD/INR/GBP/EUR, major stock index value, and its HQ map link."
        result = agent_executor.invoke({"input": task})
        st.markdown(result["output"])