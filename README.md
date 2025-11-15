# Smart URL Summarizer (Flask API)
A lightweight API that shortens URLs, tracks clicks, and generates AI summaries of webpage content.

## Features
- Shorten long URLs with unique hashes
- Redirect to original pages
- AI-based webpage summarization using Hugging Face (T5)
- Track click counts per URL

## Tech Stack
- Python
- Flask
- Hugging Face Transformers (T5-small)
- BeautifulSoup4
- JSON-based storage

## API Routes
| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/shorten` | Shorten URL and summarize webpage |
| GET | `/<short_id>` | Redirect to original page |
| GET | `/stats/<short_id>` | View analytics & summary |

## Run Locally
```bash
git clone https://github.com/infintive/smart-url-summarizer.git
cd smart-url-summarizer
pip install -r requirements.txt
python app.py
