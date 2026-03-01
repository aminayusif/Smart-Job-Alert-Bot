from ml.recommender import JobRecommender

recommender = JobRecommender()

results = recommender.recommend_jobs(
    skills="python, sql, data analysis",
    role="data analyst",
    top_n=3
)

for job in results:
    print(job)