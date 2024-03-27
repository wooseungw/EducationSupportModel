import streamlit as st
from langchain.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer. \n Please writedowm markdown language."),
    ("user", "{input}")
])

#

import os
import requests
#st.write(st.secrets.openai)

def checking_openai(api_key):
    """API 키의 유효성을 검증합니다."""
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    return response.status_code == 200

# Streamlit 세션 상태 초기화
if checking_openai(st.secrets.openai):
    st.session_state.openai_valid = True
    st.session_state.openai = st.secrets.openai

def checking_api_collback():
    if checking_openai(st.session_state.openai_api_input):
        st.session_state.api_key_valid = True
        st.session_state.openai = st.session_state.openai_api_input
        st.success("API 키가 저장되었습니다.")    
    else:
        st.error("올바른 API 키를 입력해주세요.")
        
# API 키 입력을 위한 페이지
def input_api_key():
    st.sidebar.header("OpenAI API 키 입력")
    st.sidebar.text_input(label="OpenAI API를 입력하세요",type="password", key="openai_api_input",on_change=checking_api_collback)
    
def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=st.secrets.openai)
    chain = prompt | llm 
    st.markdown(chain.invoke(input_text))
def main_page():
    with st.form('my_form'):
        text = st.text_area('Enter text:', '랭체인이 뭔가요? 3가지 장점을 설명해주세요.')
        submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)
            
input_api_key()
main_page()




