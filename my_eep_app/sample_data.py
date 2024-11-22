from pymongo import MongoClient
import random
import string

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["application_db"]

# Collections
applications_collection = db["applications"]
reviews_collection = db["reviews"]

# Helper function to generate random PSID
def generate_psid(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Helper function to generate random status
def random_status(status_list):
    return random.choice(status_list)

# Function to clean the documents in the collections
def clean_collections():
    applications_collection.delete_many({})
    reviews_collection.delete_many({})
    print("Collections cleaned successfully!")

# Clean the collections before inserting new data
clean_collections()

# Sample data for candidate applications
candidate_applications = []
for _ in range(10):
    candidate_applications.append({
        "psid": generate_psid(),
        "name": f"Candidate {_+1}",
        "last_name": f"LastName{_+1}",
        "email": f"candidate{_+1}@example.com",
        "gender": random.choice(["Male", "Female", "Other"]),
        "email_functional_manager": f"manager{_+1}@example.com",
        "tech_only_role": random.choice(["Yes", "No"]),
        "individual_or_manager": random.choice(["Individual", "Manager"]),
        "personal_statement": "I am passionate about engineering.",
        "technologies": random.sample(["Python", "Java", "C++", "C#", "JavaScript", "SQL", "NoSQL", "HTML", "CSS", "Other"], 3),
        "which_cohort": random.sample(["Cohort 1", "Cohort 2", "Cohort 3", "Cohort 4"], 1),
        "resume": None,  # Assuming no file for simplicity
        "certificate": None,  # Assuming no file for simplicity
        "status": random_status(["Draft", "Submitted", "Withdrawn"])
    })

# Insert candidate applications into MongoDB
applications_collection.insert_many(candidate_applications)

# Sample data for faculty reviews
faculty_reviews = []
for _ in range(7):
    faculty_reviews.append({
        "psid": random.choice(candidate_applications)["psid"],
        "reviewer": f"Dr. Reviewer{_+1}",
        "comments": "This is a review comment.",
        "rating": random.randint(1, 5),
        "status": random_status(["Under Review", "Approved", "Rejected"])
    })

# Insert faculty reviews into MongoDB
reviews_collection.insert_many(faculty_reviews)

print("Data populated successfully!")