from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Common resume noise words that don't help matching
NOISE_WORDS = {
    "education", "undergraduate", "expected", "linkedin", "github",
    "portfolio", "personal", "dehradun", "uttarakhand", "india",
    "institute", "technology", "management", "university", "college",
    "bachelor", "science", "email", "phone", "contact"
}

def clean_text(text):
    """Clean resume/JD text: remove emails, links, phone numbers, dates, and noise words"""
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', ' ', text)
    text = re.sub(r'\+?\d[\d\-\s]{7,}\d', ' ', text)
    text = re.sub(r'\b(19|20)\d{2}\b', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = [w for w in text.split() if w not in NOISE_WORDS]
    return ' '.join(words)

def calculate_match_score(resume_text, job_description):
    """Returns a similarity score between 0-100 using TF-IDF + cosine similarity"""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    documents = [resume_clean, jd_clean]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = round(float(similarity[0][0]) * 100, 2)

    return score

def get_missing_keywords(resume_text, job_description, top_n=10):
    """Find important JD keywords missing from the resume"""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([jd_clean])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

    keyword_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, score in keyword_scores[:top_n]]

    resume_words = set(resume_clean.split())
    missing = [kw for kw in top_keywords if kw not in resume_words]

    return missing


if __name__ == "__main__":
    resume = "Experienced Python developer skilled in Flask, SQL, and REST APIs"
    jd = "Looking for a Python developer with Flask, MongoDB, REST API, and Docker experience"

    print("Score:", calculate_match_score(resume, jd))
    print("Missing keywords:", get_missing_keywords(resume, jd))