import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import hashlib
import json
import os
import re

summarizer = pipeline("summarization", model="t5-small")

DB_PATH = "database.json"

def generate_short_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def fetch_page_text(url):
    try:
        response = requests.get(url, timeout=8, headers={
            "User-Agent": "Mozilla/5.0"
        })

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        text = clean_text(text)

        return text[:2000] if text else "No readable content found."

    except Exception as e:
        return f"Error fetching content: {e}"

def summarize_text(text):
    try:
        if len(text) < 80:
            return "Not enough content to summarize."

        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        summaries = []
        for chunk in chunks:
            s = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            summaries.append(s)

        final_input = " ".join(summaries)

        final_summary = summarizer(final_input, max_length=150, min_length=60, do_sample=False)[0]['summary_text']
        return final_summary

    except Exception as e:
        return f"Error summarizing: {e}"

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"records": []}, f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)
