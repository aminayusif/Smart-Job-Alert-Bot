import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ml.preprocess import clean_text


class JobRecommender:

    def __init__(self):
        self.vectorizer = joblib.load("ml/models/vectorizer.pkl")
        self.tfidf_matrix = joblib.load("ml/models/tfidf_matrix.pkl")
        self.df = joblib.load("ml/models/jobs_dataframe.pkl")

    def recommend_jobs(self, skills: str, role: str, top_n: int = 5):
        """
        Recommend top N jobs based on user skills and desired role.
        """

        # Combine user inputs
        user_input = f"{role} {skills}"
        user_input = clean_text(user_input)

        # Transform user input
        user_vector = self.vectorizer.transform([user_input])

        # Compute similarity
        similarity_scores = cosine_similarity(
            user_vector, self.tfidf_matrix
        )[0]

        # Get top matches
        top_indices = np.argsort(similarity_scores)[::-1][:top_n]

        results = []

        for idx in top_indices:
            results.append({
                "job_title": self.df.iloc[idx]["title"],
                "short_description": self.df.iloc[idx]["description"][:200] + "...",
                "similarity_score": round(float(similarity_scores[idx]), 3)
            })

        return results