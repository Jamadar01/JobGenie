# JobGenie

An AI-powered job recommendation system that scrapes job listings, analyzes your resume, and recommends the most relevant positions using semantic search.

## How It Works

1. **Scrape** — Pulls job listings from Indeed via Apify and stores them in MongoDB.
2. **Index** — Generates OpenAI embeddings for each job description and upserts them into a Pinecone vector index.
3. **Analyze** — Reads your resume PDF and uses GPT-4o-mini to produce a skills/experience summary.
4. **Recommend** — Runs a semantic search against the vector index using the resume summary and returns the top matching jobs.
5. **Automate** — An APScheduler job cleans up stale data and re-runs the full pipeline every Monday at 00:01 IST.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| Job Scraping | Apify (`borderline/indeed-scraper`) |
| Storage | MongoDB (pymongo) |
| Vector DB | Pinecone (`text-embedding-3-large`, cosine, 3072-dim) |
| LLM | OpenAI GPT-4o-mini |
| PDF Parsing | pdfplumber |
| Scheduler | APScheduler |
| UI | Streamlit |

## Project Structure

```
JobGenie/
├── main.py                  # FastAPI app and route definitions
├── config/
│   └── config.py            # Loads environment variables
├── services/
│   ├── jobscraping.py       # Apify scraping + job storage orchestration
│   ├── resumeanalyser.py    # Resume parsing and GPT-4o-mini analysis
│   ├── storage.py           # MongoDB CRUD for job listings
│   └── vectorstore.py       # Pinecone index management and semantic search
├── schedular/
│   └── schedular.py         # Weekly automated pipeline (APScheduler)
├── UI/
│   └── chat-ui.py           # Streamlit chat interface
└── .env                     # Environment variables (not committed)
```

## Setup

### Prerequisites

- Python 3.10+
- MongoDB running locally or a MongoDB Atlas URI
- Pinecone account
- OpenAI API key
- Apify API key

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd JobGenie

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
APIFY_API_KEY=your_apify_api_key
VECTOR_DB_URL=your_pinecone_api_key
MONGO_URI=mongodb://localhost:27017/   # optional, defaults to localhost
```

## Running the App

### Backend (FastAPI)

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`.

### Frontend (Streamlit)

```bash
streamlit run UI/chat-ui.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/getjobs` | Scrape jobs from Indeed via Apify |
| GET | `/job-storing` | Scrape, store in MongoDB, and create vector index |
| GET | `/vectorstore` | Create/update Pinecone index from stored jobs |
| GET | `/semantic-search` | Run a semantic search against the vector index |
| GET | `/recommend-jobs` | Analyze resume and return top matching jobs |
| GET | `/create-embedding-index` | Generate embeddings for a test set of sentences |

## Automated Pipeline

The scheduler runs `daily_pipeline()` every **Monday at 00:01 IST**, which:

1. Deletes all existing jobs from MongoDB and Pinecone.
2. Scrapes fresh job listings from Indeed.
3. Stores them in MongoDB and rebuilds the Pinecone index.

## Resume

Place your resume PDF in the project root named `Wajid_Jamadar_Resume.pdf` (or update the path in `services/resumeanalyser.py`). The `/recommend-jobs` endpoint will parse it and return a ranked list of matching jobs saved to `search_results_new.csv`.
