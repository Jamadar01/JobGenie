from openai import OpenAI
from config.config import openai_api_key
from services.vectorstore import VectorStoreService
from services.storage import JobStorage
import pandas as pd
client = OpenAI(api_key=openai_api_key)
import pdfplumber
class ResumeAnalyser:
    def recommend_jobs(self) -> dict:
        resume_text = ""
        with pdfplumber.open("Wajid_Jamadar_Resume.pdf") as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text()
        analysis = self.analyse_resume_summary(resume_text)
        vector_store_service = VectorStoreService()
        search_results = vector_store_service.semantic_search(analysis["summary"])
        job_storage = JobStorage()
        job_details_list = []
        for result in search_results:
            job_details = job_storage.get_job(result["id"])
            job_details["similarity_score"] = result["score"]*100
            job_details_list.append(job_details)
        Formated_search_results = [
            {
                "job_title": job.get("job_title"),
                "company_name": job.get("company_name"),
                "location": job.get("location"),
                "link": job.get("job_url"),
                "job_description": job.get("jobdescription"),
                "similarity_score": job.get("similarity_score"),
                "salary": job.get("salary"),
                "rating": job.get("rating")
            }
            for job in job_details_list
        ]
        search_df = pd.DataFrame(Formated_search_results)
        search_df.to_csv("search_results_new.csv", index=False)
        print("Search Results:>>>>>>>>>>>>>>>", Formated_search_results)
        return Formated_search_results

    def analyse_resume_summary(self, resume_text: str) -> dict:
        prompt = f"Please analyze the following resume and provide a summary of the candidate's skills, experience, and qualifications:\n\n{resume_text}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content.strip()
        return {"summary": analysis}