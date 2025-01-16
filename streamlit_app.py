import streamlit as st
from groq import Groq


client = Groq(api_key=st.secrets["API_KEY"])

def generate_prompt(user_input):
    prompt = (
        f'You are a chatbot for answering all the questions related to JNTUH\n'
        f'Only give the response that is related to the university\n'
        f"Give the output in plain text without bolding any word\n"
        f'User  Query: {user_input}\n\n'
        f'Answer the user query to the best of your knowledge.'
    )
    return prompt

def main():
    st.title("JNTUH Chatbot")
    st.write("Ask me anything related to JNTUH!")

    user_query = st.text_input("Your Question:", placeholder="Type your question here...")

    if user_query:
        prompt = generate_prompt(user_query)
        with st.spinner("Generating response..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            response = ""
            for chunk in completion:
                response_chunk = chunk.choices[0].delta.content or ""
                response += response_chunk

            st.success(response)

    st.write("Type 'exit' or 'quit' in the input box to end the session.")

if __name__ == "__main__":
    main()