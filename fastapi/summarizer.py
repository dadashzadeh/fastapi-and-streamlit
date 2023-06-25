from typing import List
from fastapi import FastAPI, Query, HTTPException, Request, Form
from fastapi_profiler import PyInstrumentProfilerMiddleware
import openai
from transformers import pipeline

# list api keys openai
api_keyss = ["api keys","api keys"]

# Create a list of tags metadata
tags_metadata = [
    {
        "name": "text summarizer with ChatGPT",
        "description": "summarize text with ChatGPT",
    },
    {
        "name": "text summarizer with model",
        "description": "summarize text with model bart-large-cnn",
    },
    {
        "name": "generate image ChatGPT",
        "description": "generate image with ChatGPT",
    },
]

# Initialize FastAPI with title, version and openapi_tags
app = FastAPI(
    title="tools",
    version="1.0",
    openapi_tags=tags_metadata
)

# check your service code performance
#ai.add_middleware(PyInstrumentProfilerMiddleware)


@app.get('/bart-large-cnn', tags=["text summarizer with model"])
async def bart_large_cnn(input: str = Query(...), max_length: int = Query(default=130), min_length: int = Query(default=30)):

    # Initialize summarizer with the BART-large-cnn model from Facebook
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Generate output text using summarizer, with max and min length specified 
    output_text = summarizer(input, max_length=max_length, min_length=min_length, do_sample=False)

    # Return the summarized text
    return {
        "summarization": output_text,
    }


@app.get('/chatgpt-summarization', tags=["text summarizer with ChatGPT"])
async def chatgpt_summarization(input: str = Query(...)):
    # Loop through all the API keys
    for keys in api_keyss:
        try:
            # Create a ChatCompletion object with the given input
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Summary of the text in English: {input}"}
                ]
            )
            # Return the summarized text
            return {"summarization": completion.choices[0].message["content"]}
        except:
            # Change the API key if an exception occurs
            openai.api_key = keys
            continue


@app.get('/chatgpt-generate-an-image', tags=["generate image ChatGPT"])
async def generate_an_image(input: str = Query(...)):
    # Loop through all the API keys
    for keys in api_keyss:
        try:
            # Create a ChatCompletion object with the given input
            response = openai.Image.create(
                size="512x512",
                n=1,
                prompt=input
            )
            # Return the image url
            return {"image_url": response['data'][0]['url']}
        except:
            # Change the API key if an exception occurs
            openai.api_key = keys
            continue
