import streamlit as st
import pandas as pd

from database import SessionLocal, Client

# Page title
st.title("Client Tracker")

# Database session
session = SessionLocal()

# Form
st.header("Add New Client")

company_name = st.text_input("Company Name")
contact_person = st.text_input("Contact Person")
phone = st.text_input("Phone")
email = st.text_input("Email")
last_contact = st.date_input("Last Contact Date")

status = st.selectbox(
    "Status",
    ["Prospect", "Contacted", "Interested", "Negotiating", "Closed"]
)

# Save button
if st.button("Save Client"):

    new_client = Client(
        company_name=company_name,
        contact_person=contact_person,
        phone=phone,
        email=email,
        status=status,
        last_contact=str(last_contact)
    )

    session.add(new_client)
    session.commit()

    st.success("Client saved successfully!")

# Display clients
st.header("All Clients")

clients = session.query(Client).all()

if clients:

    for client in clients:

        col1, col2, col3, col4 = st.columns([3, 3, 2, 1])

        with col1:
            st.write(f"**{client.company_name}**")

        with col2:
            st.write(client.contact_person)

        with col3:
            st.write(client.status)

        with col4:
            if st.button("Delete", key=client.id):
                session.delete(client)
                session.commit()
                st.rerun()

else:
    st.info("No clients added yet.")