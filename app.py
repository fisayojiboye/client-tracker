import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from modules.dashboard import show_dashboard
from modules.add_client import show_add_client
from modules.manage_clients import show_manage_clients

# PAGE CONFIG
st.set_page_config(
    page_title="Client CRM",
    layout="wide"
)

# LOAD CONFIG
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# AUTHENTICATOR
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# LOGIN
authenticator.login()

# AUTH STATUS
if st.session_state["authentication_status"]:

    authenticator.logout("Logout", "sidebar")

    st.sidebar.title("Client CRM")

    st.sidebar.success(
        f"Welcome {st.session_state['name']}"
    )

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

elif st.session_state["authentication_status"] is False:

    st.error("Incorrect Username or Password")

elif st.session_state["authentication_status"] is None:

    st.warning("Please Login")