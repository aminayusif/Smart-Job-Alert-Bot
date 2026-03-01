import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load cleaned dataset
df = pd.read_csv("data/processed/job_postings_cleaned.csv")

# Initialize TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2)
)

# Fit and transform job texts
tfidf_matrix = vectorizer.fit_transform(df["text"])

# Save artifacts
joblib.dump(vectorizer, "ml/models/vectorizer.pkl")
joblib.dump(tfidf_matrix, "ml/models/tfidf_matrix.pkl")
df.to_pickle("ml/models/jobs_dataframe.pkl")

print("Training complete. Artifacts saved.")