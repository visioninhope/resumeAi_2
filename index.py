# index.py

from services.job_description_formatter import load_and_process_documents

def main():
    vector_db = load_and_process_documents()
    # Perform a sample similarity search to test the setup
    sample_query = "list the minimum and preferred skills for this job?"
    sample_result = vector_db.similarity_search(query=sample_query)
    print("Sample Search Result:", sample_result[1].page_content)

if __name__ == "__main__":
    main()
