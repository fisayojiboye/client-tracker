import streamlit as st
from database import SessionLocal, Client

session = SessionLocal()

def show_manage_clients():

    st.title("Manage Clients")

    search = st.text_input("Search")

    status_filter = st.selectbox(
        "Status Filter",
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

    filtered = []

    for client in clients:

        matches_search = (
            search.lower() in client.company_name.lower()
            or search.lower() in client.contact_person.lower()
        ) if search else True

        matches_status = (
            client.status == status_filter
        ) if status_filter != "All" else True

        if matches_search and matches_status:
            filtered.append(client)

    for client in filtered:

        with st.expander(
            f"{client.company_name} - {client.status}"
        ):

            company = st.text_input(
                "Company",
                value=client.company_name,
                key=f"company{client.id}"
            )

            contact = st.text_input(
                "Contact",
                value=client.contact_person,
                key=f"contact{client.id}"
            )

            phone = st.text_input(
                "Phone",
                value=client.phone,
                key=f"phone{client.id}"
            )

            email = st.text_input(
                "Email",
                value=client.email,
                key=f"email{client.id}"
            )

            status = st.selectbox(
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

            notes = st.text_area(
                "Notes",
                value=client.notes,
                key=f"notes{client.id}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Update",
                    key=f"update{client.id}"
                ):

                    client.company_name = company
                    client.contact_person = contact
                    client.phone = phone
                    client.email = email
                    client.status = status
                    client.notes = notes

                    session.commit()

                    st.success("Updated Successfully")

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete{client.id}"
                ):

                    session.delete(client)
                    session.commit()

                    st.warning("Deleted")

                    st.rerun()