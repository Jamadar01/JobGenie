from fastapi import FastAPI
from services import vectorstore, resumeanalyser,jobscraping
from pymongo import MongoClient
import os
from schedular.schedular import start_scheduler, stop_scheduler
from contextlib import asynccontextmanager

mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
db = mongo_client["jobgenie"]          # database (created on first write)
jobs_collection = db["jobs"]  


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()      
    yield
    stop_scheduler()

app = FastAPI(lifespan=lifespan)
@app.get("/")
def read_root():
    return {"message": "Welcome to JobGenie API!"}

@app.get("/getjobs")
def get_jobs():
    job_genie = jobscraping.JobScrapingService()
    return job_genie.run_actors()

@app.get("/vectorstore")
def get_vectorstore():
    vector_store = vectorstore.VectorStoreService()
    return vector_store.create_index()

@app.get("/semantic-search")
def get_semantic_search():
    vector_store = vectorstore.VectorStoreService()
    return vector_store.semantic_search()

@app.get("/create-embedding-index")
def get_create_embedding_index():
    vector_store = vectorstore.VectorStoreService()
    sentences = ["The Eiffel Tower was completed in 1889 and stands in Paris, France.", "Photosynthesis allows plants to convert sunlight into energy."]
    return vector_store.create_embedding_index(sentences)

@app.get("/job-storing")
def get_job_storing():
    job_genie = jobscraping.JobScrapingService()
    return job_genie.job_storing()

@app.get("/recommend-jobs")
def get_recommend_jobs():
    resume_analyser = resumeanalyser.ResumeAnalyser()
    search_results = resume_analyser.recommend_jobs()
    print("insie route page")
    return search_results


