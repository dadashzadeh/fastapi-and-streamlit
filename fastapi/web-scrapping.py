# Importing FastAPI and Pydantic libraries
from fastapi import FastAPI
from pydantic import HttpUrl

# Importing requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup

# Creating an instance of FastAPI
app = FastAPI()

# Defining a root route


@app.get("/s")
async def root():
    return {"message": "Hello World"}

# Defining a post route to scrape tags from a given URL


@app.post('/site')
async def scrape_tags(input: HttpUrl):
    # Making a request to the given URL
    with requests.Session() as r:
        page = r.get(input)

    # Parsing the response using BeautifulSoup
    soup = BeautifulSoup(page.content, 'lxml')
    h1 = soup.find("h1").text.strip()

    # Returning the scraped data
    return {
        "h1": h1,
    }
