import streamlit as st
import pandas as pd
from datetime import date

from database import SessionLocal, Client

# Database session
session = SessionLocal()

# PAGE CONFIG
st.set_page_config(
    page_title="Client CRM",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    ["Dashboard", "Add Client", "Manage Clients"]
)

# DASHBOARD PAGE
if page == "Dashboard":

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

    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Clients", total_clients)
    col2.metric("Interested", interested)
    col3.metric("Negotiating", negotiating)
    col4.metric("Closed Deals", closed)

    st.divider()

    # FOLLOW UPS
    st.subheader("Upcoming Follow-Ups")

    today = str(date.today())

    followups = [
        c for c in clients
        if c.next_follow_up and c.next_follow_up <= today
    ]

    if followups:

        for client in followups:

            st.warning(
                f"{client.company_name} "
                f"needs follow-up today."
            )

    else:
        st.success("No pending follow-ups.")

# ADD CLIENT PAGE
elif page == "Add Client":

    st.title("Add New Client")

    company_name = st.text_input("Company Name")

    contact_person = st.text_input("Contact Person")

    phone = st.text_input("Phone")

    email = st.text_input("Email")

    status = st.selectbox(
        "Status",
        [
            "Prospect",
            "Contacted",
            "Interested",
            "Negotiating",
            "Closed"
        ]
    )

    last_contact = st.date_input(
        "Last Contact Date"
    )

    next_follow_up = st.date_input(
        "Next Follow-Up Date"
    )

    notes = st.text_area("Notes")

    if st.button("Save Client"):

        new_client = Client(
            company_name=company_name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            status=status,
            last_contact=str(last_contact),
            next_follow_up=str(next_follow_up),
            notes=notes
        )

        session.add(new_client)
        session.commit()

        st.success("Client Added Successfully!")

# MANAGE CLIENTS PAGE
elif page == "Manage Clients":

    st.title("Manage Clients")

    # SEARCH
    search = st.text_input(
        "Search Client"
    )

    status_filter = st.selectbox(
        "Filter By Status",
        [
            "All",
            "Prospect",
            "Contacted",
            "Interested",
            "Negotiating",
            "Closed"
        ]
    )

    clients = session.query(Client).all()

    filtered_clients = []

    for client in clients:

        matches_search = (
            search.lower() in client.company_name.lower()
            or search.lower() in client.contact_person.lower()
        ) if search else True

        matches_status = (
            client.status == status_filter
        ) if status_filter != "All" else True

        if matches_search and matches_status:
            filtered_clients.append(client)

    # DISPLAY CLIENTS
    for client in filtered_clients:

        with st.expander(
            f"{client.company_name} - {client.status}"
        ):

            # EDIT FIELDS
            new_company = st.text_input(
                "Company",
                value=client.company_name,
                key=f"company{client.id}"
            )

            new_contact = st.text_input(
                "Contact Person",
                value=client.contact_person,
                key=f"contact{client.id}"
            )

            new_phone = st.text_input(
                "Phone",
                value=client.phone,
                key=f"phone{client.id}"
            )

            new_email = st.text_input(
                "Email",
                value=client.email,
                key=f"email{client.id}"
            )

            new_status = st.selectbox(
                "Status",
                [
                    "Prospect",
                    "Contacted",
                    "Interested",
                    "Negotiating",
                    "Closed"
                ],
                index=[
                    "Prospect",
                    "Contacted",
                    "Interested",
                    "Negotiating",
                    "Closed"
                ].index(client.status),
                key=f"status{client.id}"
            )

            new_notes = st.text_area(
                "Notes",
                value=client.notes,
                key=f"notes{client.id}"
            )

            col1, col2 = st.columns(2)

            # UPDATE BUTTON
            with col1:
                if st.button(
                    "Update",
                    key=f"update{client.id}"
                ):

                    client.company_name = new_company
                    client.contact_person = new_contact
                    client.phone = new_phone
                    client.email = new_email
                    client.status = new_status
                    client.notes = new_notes

                    session.commit()

                    st.success("Client Updated!")

            # DELETE BUTTON
            with col2:
                if st.button(
                    "Delete",
                    key=f"delete{client.id}"
                ):

                    session.delete(client)
                    session.commit()

                    st.warning("Client Deleted")

                    st.rerun()