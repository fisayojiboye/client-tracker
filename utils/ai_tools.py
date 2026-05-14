from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY"
)

def generate_followup(client_name, status):

    prompt = f"""
    Write a professional follow-up message
    for a prospect named {client_name}.

    Their current status is {status}.

    Keep it concise and persuasive.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content