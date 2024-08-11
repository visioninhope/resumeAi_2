# match_grader.py
from typing import Dict, List
from datetime import datetime

def parse_dates(date_str):
    # Parses dates in the format 'Month YYYY'
    return datetime.strptime(date_str, "%b %Y")

def calculate_experience(text: str) -> int:
    return text.split(',')


def extract_skills(text: str) -> List[str]:
    # Dummy implementation for example; replace with your actual parsing logic
    return text.split(',')

def extract_frameworks(text: str) -> List[str]:
    return text.split(',')

def extract_databases(text: str) -> List[str]:
    return text.split(',')

def extract_cloud_platforms(text: str) -> List[str]:
    return text.split(',')

def extract_programming_languages(text: str) -> List[str]:
    # This function should parse out programming languages from the text
    return text.split(',')

def prepare_data(page_content: str) -> Dict[str, List[str]]:
    return {
        'skills': extract_skills(page_content),
        'frameworks': extract_frameworks(page_content),
        'databases': extract_databases(page_content),
        'cloud': extract_cloud_platforms(page_content),
        'programming_languages': extract_programming_languages(page_content)
    }

def evaluate_match(job_description_content: str, profile_content: str) -> str:
    job_description = prepare_data(job_description_content)
    profile = prepare_data(profile_content)

    # Check for at least one match in programming languages if specified
    if 'programming_languages' in job_description and job_description['programming_languages']:
        if not any(lang in profile['programming_languages'] for lang in job_description['programming_languages']):
            return "No"

    # Check for at least one match in skills/programming languages
    if not any(skill in profile['skills'] for skill in job_description['skills']):
        return "No"

    # Check for at least one match in frameworks if frameworks are specified in the job description
    if 'frameworks' in job_description and job_description['frameworks']:
        if not any(framework in profile['frameworks'] for framework in job_description['frameworks']):
            return "No"

    # Check for at least one match in databases if databases are specified in the job description
    if 'databases' in job_description and job_description['databases']:
        if not any(database in profile['databases'] for database in job_description['databases']):
            return "No"

    # Check for at least one match in cloud platforms if cloud platforms are specified in the job description
    if 'cloud' in job_description and job_description['cloud']:
        if not any(cloud in profile['cloud'] for cloud in job_description['cloud']):
            return "No"
    
    if 'experience' in job_description and job_description['experience']:
        if not any(experience in profile['experience'] for experience in job_description['experience']):
            return "No"

    return "Yes"
