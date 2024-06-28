import streamlit as st # type: ignore
from hugchat import hugchat # type: ignore
from hugchat.login import Login # type: ignore

st.title('Simple ChatBot')

with st.sidebar:
    st.title('Login HugChat')
    hf_email = st.text_input('Enter E-mail:')
    hf_pass = st.text_input('Enter Password:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Please enter your account!')
    else:
        st.success('Proceed to entering your prompt message!')

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': 'How may I help you?'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

prompt = st.chat_input("Enter your message:", disabled=not (hf_email and hf_pass))
if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)

if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            response = generate_response(st.session_state.messages[-1]['content'], hf_email, hf_pass)
            st.write(response)
    message = {'role': 'assistant', 'content': response}
    st.session_state.messages.append(message)
