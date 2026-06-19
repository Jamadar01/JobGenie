# Import the Pinecone library
from pinecone import Pinecone,ServerlessSpec
from config.config import vector_db_url,openai_api_key
import time
from openai import OpenAI
from services.storage import JobStorage

client = OpenAI(api_key=openai_api_key)
    
pc = Pinecone(api_key=vector_db_url)

class VectorStoreService:
    def create_embedding_index(self,records):
        for record in records:
            sentences = [record["jobdescription"]]
            embeddings = client.embeddings.create(
                model="text-embedding-3-large",
                input=sentences
            )
            record["values"] = embeddings.data[0].embedding
        return records

    def create_index(self):
        index_name = "jobgenie-rag"
        if not pc.has_index(index_name):
            pc.create_index(
                name=index_name,
                dimension=3072,            
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )

        job_storage = JobStorage()
        records = job_storage.get_all_jobs()
        result=self.create_embedding_index(records)
        dense_index = pc.Index(index_name)

        vectors = [{
            "id": str(record["_id"]),
            "values": record["values"],
            "metadata": {
                "job_title": record["job_title"],
                "jobdescription": record["jobdescription"]
            }
        } for record in result
        ]
        dense_index.upsert(vectors=vectors, namespace="jobs-listings")
        print(vectors[0]['metadata'])
        time.sleep(10)
        stats = dense_index.describe_index_stats()
        print(stats)
    
    def semantic_search(self, query):
        index_name = "jobgenie-rag"
        embeddings = self.create_embedding_index([{"jobdescription": query}])
        dense_index = pc.Index(index_name)

        # Search the index
        results = dense_index.query(
            namespace="jobs-listings",
            vector=embeddings[0]["values"],
            top_k=10,
            include_metadata=True,
        )
        results = results.to_dict()

        print("Results:>>>>>>>>>>>>>>>", results)
        
        return results["matches"]
        # Print the results
