import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import hashlib
import json
import os
import re

DB_PATH = "database.json"
summarizer = None   # lazy load T5-small only once


def load_summarizer():
    """Load the T5-small summarizer only once (important for Render)."""
    global summarizer
    if summarizer is None:
        summarizer = pipeline("summarization", model="t5-small")
    return summarizer


def generate_short_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:6]


def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fetch_page_text(url):
    """Extract readable text from webpage."""
    try:
        print("[DEBUG] Fetching:", url)

        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })

        soup = BeautifulSoup(response.text, "lxml")

        # Remove noise
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ")
        text = clean_text(text)

        print("[DEBUG] Extracted text length:", len(text))

        # Avoid overloading T5-small
        return text[:2500] if len(text) > 0 else "No readable content found."

    except Exception as e:
        return f"Error fetching content: {e}"


def summarize_text(text):
    """Summarize long text using T5-small with chunking."""
    try:
        print("[DEBUG] Summarizing text...")

        summarizer_model = load_summarizer()

        if len(text) < 80:
            return "Not enough content to summarize."

        chunk_size = 1000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        print(f"[DEBUG] Total chunks: {len(chunks)}")

        chunk_summaries = []

        for idx, chunk in enumerate(chunks):
            print(f"[DEBUG] Summarizing chunk {idx + 1}/{len(chunks)}")

            summary = summarizer_model(
                chunk,
                max_length=150,
                min_length=50,
                do_sample=False
            )[0]['summary_text']

            chunk_summaries.append(summary)

        combined_text = " ".join(chunk_summaries)

        print("[DEBUG] Generating final summary...")

        final_summary = summarizer_model(
            combined_text,
            max_length=150,
            min_length=60,
            do_sample=False
        )[0]['summary_text']

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
