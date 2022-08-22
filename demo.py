import streamlit as st
import requests

st.header("anonymization-app")
st.markdown("Remove personally identifiable information from text.")
st.markdown("Built with love by [NLRC 510](https://www.510.global/). See [the project on GitHub](https://github.com/rodekruis/anonymization-app).")
text = st.text_area('Input', 'Hello my name is Anna and my phone number is +12345678910.')
submit = st.button('Anonymize')
if submit:

    url = 'https://anonymization-app.azurewebsites.net/anonymize/'
    payload = {'text': text}

    with st.spinner(text="This may take a moment..."):
        result = requests.post(url, json=payload).json()
        if 'anonymized_text' in result.keys():
            text = result['anonymized_text']
        else:
            text = "An error occurred, please try again later or [contact us](mailto:support@510.global)!"

    st.text_area('Output', text)