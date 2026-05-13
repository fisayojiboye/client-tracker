import streamlit as st
from datetime import date
from database import SessionLocal, Client
import plotly.express as px
import pandas as pd

session = SessionLocal()

def show_dashboard():

    st.title("CRM Dashboard")

    clients = session.query(Client).all()

    total_clients = len(clients)

    interested = len(
        [c for c in clients if c.status == "Interested"]
    )

    negotiating = len(
        [c for c in clients if c.status == "Negotiating"]
    )

    closed = len(
        [c for c in clients if c.status == "Closed"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Clients", total_clients)
    col2.metric("Interested", interested)
    col3.metric("Negotiating", negotiating)
    col4.metric("Closed", closed)

    st.divider()

    st.subheader("Today's Follow-Ups")

    today = str(date.today())

    followups = [
        c for c in clients
        if c.next_follow_up
        and c.next_follow_up <= today
    ]

    if followups:

        for client in followups:

            st.warning(
                f"{client.company_name} requires follow-up."
            )

    else:
        st.success("No follow-ups due.")