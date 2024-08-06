# index.py

from services.job_description_formatter import load_and_process_documents
from services.profile import process_profile  # Make sure this import statement correctly points to the function
from pymilvus import connections, Collection,MilvusClient
import time  # Import the time module at the beginning of your script


def main():

    client = MilvusClient( host='127.0.01', port='19530')
    # Load and process job description data, storing results in a Milvus collection
    vector_db_job_desc = load_and_process_documents()
    
    # Load and process personal profile data, storing results in a separate Milvus collection
    vector_db_profile = process_profile()

    # # Perform a sample similarity search on the job description data
    job_desc_query = "list the minimum and preferred skills for this job?"
    job_desc_query_answer = vector_db_job_desc.similarity_search(query=job_desc_query)
        # Check and print job description skills
    if job_desc_query_answer:
        if len(job_desc_query_answer) > 1:
                print("Job Description Skills:", job_desc_query_answer[1].page_content)
        else:
                print("Job Description Skills:", job_desc_query_answer[0].page_content)
    else:
            print("No results found for job description skills.")

    # Perform a sample similarity search on the profile data
    profile_desc_query = "list all the technical skills of this profile"
    profile_desc_query_answer = vector_db_profile.similarity_search(query=profile_desc_query)
    print("Profile Skills:", profile_desc_query_answer[1].page_content)


    # # Drop the collections after the similarity search
    client.drop_collection("job_description_after_formatting")


if __name__ == "__main__":
    main()
