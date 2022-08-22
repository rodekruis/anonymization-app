import streamlit as st
import requests

st.subheader("Output")
url = 'https://anonymization-app.azurewebsites.net/'
myobj = {'text': 'Hello my name is Anna and my phone number is +12345678.'}
x = requests.post(url, json=myobj)
print(x)

# st.header("anonymization-app")
# st.subheader("Input")
# text = st.text_area('', 'Hello my name is Anna and my phone number is +12345678.')
# submit = st.button('Remove personally identifiable information')
# if submit:
#
#     st.subheader("Output")
#     url = 'https://anonymization-app.azurewebsites.net/'
#     myobj = {'text': text}
#
#     with st.spinner(text="This may take a moment..."):
#         x = requests.post(url, json=myobj)
#
#     st.write(x.text)