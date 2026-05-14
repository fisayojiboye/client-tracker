import requests

def generate_clean_excel(client_data):

    url = "YOUR_CLARE_API_ENDPOINT"

    payload = {
        "company_name": client_data.company_name,
        "contact_person": client_data.contact_person,
        "phone": client_data.phone,
        "email": client_data.email,
        "status": client_data.status,
        "last_contact": client_data.last_contact,
        "next_follow_up": client_data.next_follow_up,
        "notes": client_data.notes
    }

    response = generate_clean_excel(client)

    if response.status_code == 200:

        return response