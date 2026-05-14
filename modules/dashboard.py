import streamlit as st
from datetime import date
from database import SessionLocal, Client
import plotly.express as px
import pandas as pd
from database import Activity

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

    st.subheader("Pipeline Analytics")

    status_counts = {}

    for client in clients:

     if client.status in status_counts:
        status_counts[client.status] += 1

    else:
        status_counts[client.status] = 1

    df = pd.DataFrame({
    "Status": list(status_counts.keys()),
    "Count": list(status_counts.values())
   })

    fig = px.pie(
    df,
    names="Status",
    values="Count",
    title="Client Pipeline"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

st.subheader("Recent Activities")

activities = (
    session.query(Activity)
    .order_by(Activity.id.desc())
    .limit(10)
    .all()
)

for activity in activities:

    st.write(
        f"{activity.timestamp} - "
        f"{activity.client_name} - "
        f"{activity.action}"
    )

    