# Importing necessary libraries
import streamlit as st
from bs4 import BeautifulSoup
import requests
from PIL import Image

# Creating a title for the web page
st.title('Web Scraping')

# Adding a markdown to explain the purpose of the code
st.markdown('''<p style="text-align: center;">get data web site</p>''',
            unsafe_allow_html=True)

# Creating a form to get the URL from the user
form = st.form(key='my_form')
url = form.text_input(label='Enter some url')
submit_button = form.form_submit_button(label='Submit')

# If the submit button is clicked, execute the following code
if submit_button:
    # Creating a header for the request
    header = {'user-agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36',
              'Referer': 'https://google.com/'}

    # Making a request to the given URL
    response = requests.get(url, headers=header)

    # Parsing the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    # Finding the meta tag with property og:image
    image = soup.find("meta", {"property": "og:image"})["content"]

    # Writing the title, h1 and description to the web page
    st.write(f'title = {soup.title.text}')
    st.write(f'h1 = {soup.h1.text}')
    st.write(
        f'description = {soup.find("meta" , {"name": "description"})["content"]}')

    # Opening the image from the URL and displaying it on the web page
    image = Image.open(requests.get(image, stream=True).raw)
    st.image(image)
