from fastapi import FastAPI
from ml.recommender import JobRecommender

app = FastAPI()

# Load recommender once
recommender = JobRecommender()


@app.get("/")
def home():
    return {"message": "JobSenseBot API is running 🚀"}


@app.post("/recommend")
def recommend(data: dict):
    skills = data.get("skills", "")
    role = data.get("role", "")

    results = recommender.recommend_jobs(
        skills=skills,
        role=role,
        top_n=5
    )

    return results