import streamlit as st

from modules.dashboard import show_dashboard
from modules.add_client import show_add_client
from modules.manage_clients import show_manage_clients

st.set_page_config(
    page_title="Client CRM",
    layout="wide"
)

st.sidebar.title("Client CRM")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Client",
        "Manage Clients"
    ]
)

if page == "Dashboard":
    show_dashboard()

elif page == "Add Client":
    show_add_client()

elif page == "Manage Clients":
    show_manage_clients()