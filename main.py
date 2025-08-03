import streamlit as st
from PIL import Image
import base64
import threading
import warnings
import requests
import time
import urllib
from streamlit_cookies_manager import EncryptedCookieManager

warnings.filterwarnings("ignore", category=DeprecationWarning)

cookies = EncryptedCookieManager(password="EvolvrTest121212")
redirect_url='https://google.com'

#Box + Header

st.markdown(
    """
    <style>
    .form-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .header-image {
        width: 100%;
        border-radius: 15px 15px 0 0;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        color: gray;
        font-size: 0.9em;
    }
    .footer a {
        color: gray;
        text-decoration: none;
    }
    .footer a:hover {
        color: #1e88e5;
    }
    .title {
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.5em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True)

#Redirect Function

def redirect(url):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url={url}">
        <script>
            window.location.href = "{url}"
        </script>
    """, unsafe_allow_html=True)

#Forms

with st.form("contest_form"):
    with st.container():
        try:
            st.image("pic1.jpg", use_container_width=True, output_format="auto", 
                    caption="", clamp=True, channels="RGB")
        except:
            st.warning("Header image not found")
    st.markdown('<div class="title">Enter your information to stand a chance to enjoy a fine dining experience on us</div>', 
               unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("Full Name")
        last_name = st.text_input("Last Name")
        phone_number = st.text_input("Phone Number")
        
    submitted = st.form_submit_button("Menu")
    st.markdown('</div>', unsafe_allow_html=True)

#Error Trial

if cookies.ready():
    if cookies.get("form_filled") == "true":
        redirect(redirect_url)
        st.stop()

if submitted:
    for i in first_name:
        if i is int:
            st.error("First name cannot contain any numbers")
    for i in last_name:
        if i is int:
            st.error("Last name cannot contain any numbers")
    if first_name=='':
        st.error('Please enter your first name')
    if last_name=='':
        st.error('Please enter your last name')
    elif phone_number[0]!='+' and len(phone_number)!=8:
        st.error('Please enter a valid phone number')

#Sucess 
    
    else:
        st.success('Redirecting you to the menu')
        for i in range(len(first_name)):
                first_name = first_name.replace(" ", "+")
        print(first_name)

        for j in range(len(phone_number)): 
                phone_number = phone_number.replace(" ", "")
        print(phone_number)

        cookies["form_filled"] = "true"
        cookies.save()

#Webhook 

        webhook=f"https://evolvrkevin.app.n8n.cloud/webhook/data?firstname={first_name}&lastname={last_name}&number={phone_number}"
        try:

# Trigger the webhook in the background

            requests.get(webhook, timeout=5)
        except Exception as e:
            print(f"Webhook call failed: {e}")

#Redirect

        redirect(redirect_url)

        