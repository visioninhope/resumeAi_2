# index.py

from services.job_description_formatter import load_and_process_documents  # Make sure this import statement correctly points to the function
from services.profile import process_profile,check_collection_exists  # Make sure this import statement correctly points to the function
from pymilvus import connections, Collection,MilvusClient
import time  # Import the time module at the beginning of your script



def main():

    client = MilvusClient( host='127.0.0.1', port='19530')
    # Load and process job description data, storing results in a Milvus collection
    vector_db_job_desc = load_and_process_documents()
    
    # Load and process personal profile data, storing results in a separate Milvus collection
    # vector_db_profile = process_profile()

    # # Perform a sample similarity search on the job description data
    job_desc_query = "list the minimum and preferred skills for this job?"
    job_desc_query_answer = vector_db_job_desc.similarity_search(query=job_desc_query)
        # Check and print job description skills
    if job_desc_query_answer:
        print("Job Description Skills:", job_desc_query_answer[0].page_content)  # Safely access the first result
    else:
        print("No results found for job description skills.")


    profile_collection_name = input("Enter the profile collection name: ")
    vector_db_profile = None  # Initialize to None
    
    # Check if the collection already exists
    if check_collection_exists(profile_collection_name):
        # Load the existing collection
        # vector_db_profile = load_profile_collection(profile_collection_name) // does not work
        print("Collection already exists and loading does not work " )
    else:
        # Load and process personal profile data, storing results in a separate Milvus collection
        vector_db_profile = process_profile(profile_collection_name)

    # Perform a sample similarity search on the profile data
    profile_desc_query = "list all the technical skills of this profile"
    profile_desc_query_answer = vector_db_profile.similarity_search(query=profile_desc_query)

    # Check and print profile skills
    if profile_desc_query_answer:
        print("Profile Skills:", profile_desc_query_answer[0].page_content)  # Safely access the first result
    else:
        print("No results found for profile skills.")

    # Drop the collections after the similarity search
    client.drop_collection("job_description_after_formatting")
    client.drop_collection(profile_collection_name)


if __name__ == "__main__":
    main()
    
