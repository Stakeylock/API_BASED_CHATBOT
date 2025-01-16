import streamlit as st
from groq import Groq


client = Groq(api_key=st.secrets["API_KEY"])
data = """GENERAL INFORMATION FOR OBTAINING DIFFERENT CERTIFICATES
S.NO	Certificate Name	Supporting Documents/Copies to be submitted	Amount	Download Forms
1	Duplicate Marks Memo / Duplicate CMM	Studying Candidates:
a) Filled in Form-1.
Course Completed Candidates:
a) Request letter from the candidate along with the Self Affidavit (Form-1A) on Rs.20/- Bond paper.
b) Photostat copies of SSC & Aadhaar Card.
c) Softcopy of passport size photograph in CD.
Rs. 200/-	Form-1

Form-1A
2	Original Degree Certificate(Passed out candidates before 2002)	a) Filled in Form-2.
b) Photostat copy of PC.
c) Photostat copies of SSC & Aadhaar Card.
d) Softcopy of passport size photograph in CD or DVD.
Rs. 1000/- + Late fee of Rs. 500/- per year	Form-2
3	Duplicate Degree Certificate	a) Filled in Form-2.
b) Filled in Form-2A.
c) Original copy of Police Report stating the original degree certificate is not traced.
d) Affidavit (Form-2A) on Rs.20/- Bond paper.
e) Photostat copy of PC/OD Certificate.
f) Photostat copies of SSC & Aadhaar Card.
g) Softcopy of passport size photograph in CD or DVD.
Rs. 10,000/-	Form-2

Form-2A
4	Name and /or Father Name and/or Gender correction in Original Degree certificate	a) Filled in Form-3.
b) Request letter from the student along with address.
c) Original Degree Certificate.
d) Original Provisional Certificate.
e) Photostat copies of SSC & Aadhaar Card.
f) Softcopy of passport size photograph in CD or DVD.
Rs. 500/-	Form-3
5	Name and /or Father Name and/or Gender correction in PC	Permitted only if the convocation is not held
a) Filled in Form-3
b) Request letter from the student.
c) Original PC.
d) Photostat copies of SSC & Aadhaar Card.
Rs. 250/-	Form-3
6	Name Corrections in Marks Memo/CMM	a) Filled in Form-3.
b) Request letter from the student.
c) Original Mark Memo/CMM.
d) Photostat copies of SSC & Aadhaar Card.
e) Softcopy of passport size photograph in CD or DVD.
Rs. 50/- per each memo	Form-3
7	Transcripts B.Tech (Admitted after 1999). M.Tech, MBA, MCA, B.Phamay, M.Pharm (Admitted after 2009)	a) Filled in Form-4	Rs. 60/- per each copy	Form-4
8	Transcripts B.Tech (Admitted before 1999). M.Tech, MBA, MCA, M.Pharm, B.Phamay (Admitted before 2009)	a) Filled in Form-4
b) Photostat copy of OD/PC/CMM/Marks memo, signed (on bottom left-side) by the Principal on each copy along with stamp.	Rs. 60/- per each copy	Form-4
9	PC and CMM With Grace Marks	a) Filled in Form-5.
b) Photostat copy of SSC.
c) Original Marks Memo(s) containing subject(s) for which award of Grace Marks requested.	Paid at college	Form-5
10	PC and CMM With Undertaking	a) Filled in form-6
b) Photostat copy of SSC	Paid at college	Form-6
11	PC and CMM With Grace Marks and Undertaking	a) Filled in form-7
b) Photostat copy of SSC
c) Original Marks Memo(s) containing subject(s) for which award of Grace Marks requested.	Paid at college	Form-7
Note:
1. The payments can be made in one of the following modes: Smart-card swiping/ T-Wallet/ SBI Challan / DD
2. If Demand Draft is taken, it should be drawn in favor of THE REGISTRAR JNTUH, payable at Hyderabad. The student Hall-Ticket number should be written on the backside of DD.
3. If the student desires to choose challan option, the challan should be taken only at the campus SBI (JNTU Hyderabad) Branch.
4. The T-Wallet/ Swiping facility using the smart card (debit/credit card) is available at the student service counter."""

def generate_prompt(user_input):
    prompt = (
        f'You are a chatbot for answering all the questions related to JNTUH\n'
        f'Only give the response that is related to the university\n'
        f"Give the output without bolding any word and give it in steps/points (only when required)\n"
        f"The data from the website is given as {data}"
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