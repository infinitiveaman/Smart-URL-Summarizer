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
Screenshots
<img width="1919" height="1079" alt="Screenshot 2025-11-23 222924" src="https://github.com/user-attachments/assets/d481ef1c-cdf7-45a8-a1d9-b302136421b5" /> <img width="1907" height="968" alt="Screenshot 2025-11-23 223141" src="https://github.com/user-attachments/assets/bfb28dfd-cd07-4f92-8591-9b818eb09be3" /> <img width="1919" height="1016" alt="Screenshot 2025-11-23 223203" src="https://github.com/user-attachments/assets/04d9c7ac-04df-4086-ad5a-ecdc33e0be0a" />
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


