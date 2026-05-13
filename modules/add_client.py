import streamlit as st
from database import SessionLocal, Client

session = SessionLocal()

def show_add_client():

    st.title("Add Client")

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

        client = Client(
            company_name=company_name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            status=status,
            last_contact=str(last_contact),
            next_follow_up=str(next_follow_up),
            notes=notes
        )

        session.add(client)
        session.commit()

        st.success("Client Added Successfully!")