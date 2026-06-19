from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
apify_api_key = os.getenv("APIFY_API_KEY")
vector_db_url = os.getenv("VECTOR_DB_URL")