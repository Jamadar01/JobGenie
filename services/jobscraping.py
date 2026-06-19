from apify_client import ApifyClient
from config.config import apify_api_key
from services.vectorstore import VectorStoreService
from services.storage import JobStorage
client = ApifyClient(token=apify_api_key)
class JobScrapingService:
    actors_to_run = [
        # {
        #     'id': 'fantastic-jobs/advanced-linkedin-job-search-api',
        #     'input': {
        #         "aiHasSalary": False,
        #         "aiVisaSponsorshipFilter": False,
        #         "directApply": False,
        #         "excludeATSDuplicate": False,
        #         "hasSalary": False,
        #         "noDirectApply": False,
        #         "populateAiRemoteLocation": False,
        #         "populateAiRemoteLocationDerived": False,
        #         "recruiterOnly": False,
        #         "remote": False,
        #         "removeAgency": False
        #     }
        # },
        {
            'id': 'borderline/indeed-scraper',
            'input': {
                "country": "us",
                "enableUniqueJobs": False,
                "includeSimilarJobs": False,
                "maxRows": 1,
                "query": "Analyst"
            }
        },
    ]

    def run_actors(self):
        all_results = []

        for actor in self.actors_to_run:
            print(f"Running Actor: {actor['id']}")
            
            run = client.actor(actor['id']).call(run_input=actor['input'])

            if run is None:
                print(f"Actor {actor['id']} failed.")
                continue

            items = client.dataset(run['defaultDatasetId']).list_items().items
            print(f"Got {len(items)} results from {actor['id']}")
            all_results.extend(items)

        print(f"Total results: {len(all_results)}")
        return all_results

    def job_storing(self):
        all_results = self.run_actors()
        print(all_results[0])
        companies = [
            {
                "company_name": result.get("companyName"),
                "job_title": result.get("title"),
                "jobdescription": result.get("descriptionText"),
                "job_type": result.get("jobType"),
                "location": result.get("location"),
                "emails": result.get("emails"),
                "company_address": result.get("companyAddresses"),
                "job_url": result.get("jobUrl"),
                "salary": result.get("salary"),
                "expired": result.get("expired"),
                "url": result.get("companyUrl"),
                "rating": result.get("rating"),
            }
            for result in all_results
        ]

        job_storage = JobStorage()
        job_storage.store_jobs(companies)

        vector_store_service = VectorStoreService()
        vector_store=vector_store_service.create_index()
        return all_results
