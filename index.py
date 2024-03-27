import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer. \n\
        Please writedowm markdown language.\n\
        And always speak Korean."),
    ("user", "{input}")
])
import os
import requests
#st.write(st.secrets.openai)

def checking_openai(api_key):
    """API 키의 유효성을 검증합니다."""
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    return response.status_code == 200

# state를 이용한 API 키 유효성 검사
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
    st.session_state.openai = ""

if checking_openai(st.secrets.openai):
    st.session_state.api_key_valid = True
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
    
# Langchain을 이용한 답변 생성, 프롬프트 연결
def generate_response(text):
    if st.session_state.api_key_valid:
        output_parser = StrOutputParser()
        llm = ChatOpenAI(openai_api_key=st.session_state.openai)
        chain = prompt | llm | output_parser
        st.markdown(chain.invoke(text))
        
def main_page():
    with st.form('my_form'):
        text = st.text_area('Enter text:', 'ex) CNN이 뭔가요? 어떤 원리인지 설명해주세요.')
        submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)
            
input_api_key()
main_page()




