from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

TECH_PHRASES = [
    # Spaced versions
    "machine learning", "deep learning", "computer vision",
    "natural language processing", "data structures", "rest apis",
    "ci/cd", "sentence transformers", "sentence bert", "s-bert",
    "transfer learning", "large language models", "generative ai",
    "responsible ai", "object detection", "neural networks",
    "reinforcement learning", "data analysis", "data analytics",
    "cloud platforms", "model deployment", "semantic similarity",
    "cosine similarity", "node.js", "react.js", "express.js",
    "tailwind css", "socket.io", "hugging face", "scikit-learn",
    "power bi", "hugging face spaces",

    # Merged versions (no space)
    "machinelearning", "deeplearning", "computervision",
    "naturallanguageprocessing", "datastructures",
    "sentencetransformers", "transferlearning", "generativeai",
    "responsibleai", "modeldeployment", "semanticsimilarity",
    "cosinesimilarity", "tailwindcss", "huggingface", "scikit learn"
]

# Normalize merged phrases to their spaced versions
PHRASE_NORMALIZE = {
    "machinelearning": "machine learning",
    "deeplearning": "deep learning",
    "computervision": "computer vision",
    "naturallanguageprocessing": "natural language processing",
    "datastructures": "data structures",
    "sentencetransformers": "sentence transformers",
    "transferlearning": "transfer learning",
    "generativeai": "generative ai",
    "responsibleai": "responsible ai",
    "modeldeployment": "model deployment",
    "semanticsimilarity": "semantic similarity",
    "cosinesimilarity": "cosine similarity",
    "tailwindcss": "tailwind css",
    "huggingface": "hugging face",
    "scikit learn": "scikit-learn"
}

STOPWORDS = {
    "and", "the", "for", "with", "that", "this", "are", "was", "have", "has",
    "will", "you", "your", "our", "from", "not", "but", "they", "their", "can",
    "also", "all", "any", "been", "more", "into", "about", "such", "than", "then",
    "when", "which", "while", "who", "how", "its", "use", "used", "using", "a",
    "an", "in", "is", "it", "of", "to", "we", "be", "as", "at", "by", "or",
    "on", "if", "do", "so", "up", "he", "she"
}

JD_NOISE = {
    "looking", "candidate", "bonus", "preferred", "required", "familiarity",
    "experience", "hands", "strong", "plus", "like", "should", "knowledge",
    "ability", "team", "work", "years", "role", "skills", "good", "well",
    "must", "need", "etc", "new", "key", "high", "level", "based",
    "build", "develop", "design", "implement", "manage", "ensure", "provide",
    "between", "following", "including", "across", "within", "through",
    "both", "each", "where", "either",
    # Single words that are part of multi-word phrases — remove as standalone
    "deep", "machine", "computer", "learning", "data", "model",
    "semantic", "sentence", "cloud", "rest", "transfer", "vision",
    "transformers", "similarity", "structures", "platforms",
    "engineer", "apis", "deployment", "pipelines"
}

def normalize_text(text: str) -> str:
    # Insert space between camelCase merged words
    spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # combine original + spaced so nothing is lost
    combined = text + " " + spaced
    return combined.lower()

def extract_keywords(text: str) -> set:
    found = set()

    # Extract multi-word tech phrases first
    for phrase in TECH_PHRASES:
        if phrase in text:
            # Normalize to spaced version
            normalized = PHRASE_NORMALIZE.get(phrase, phrase)
            found.add(normalized)

    # Extract single words
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#\.]*\b', text)
    for w in words:
        if w not in STOPWORDS and len(w) > 2:
            found.add(w)

    return found

def match_resume_jd(resume_text: str, jd_text: str) -> dict:
    # Normalize both texts
    resume_normalized = normalize_text(resume_text)
    jd_normalized = jd_text.lower()

    # Semantic similarity via S-BERT
    resume_embedding = model.encode([resume_normalized])
    jd_embedding = model.encode([jd_normalized])
    semantic_score = float(cosine_similarity(resume_embedding, jd_embedding)[0][0])

    # Keyword extraction
    resume_keywords = extract_keywords(resume_normalized)
    jd_keywords = extract_keywords(jd_normalized)

    # Remove noise from JD keywords
    jd_keywords_clean = jd_keywords - JD_NOISE

    common_keywords = jd_keywords_clean & resume_keywords
    missing_keywords = jd_keywords_clean - resume_keywords

    keyword_score = len(common_keywords) / len(jd_keywords_clean) if jd_keywords_clean else 0.0

    # 60% semantic + 40% keyword
    combined_score = (0.6 * semantic_score) + (0.4 * keyword_score)
    percentage = round(combined_score * 100, 2)

    # Feedback
    feedback = []
    if percentage >= 75:
        feedback.append("Strong match! Your resume aligns very well with this job description.")
    elif percentage >= 55:
        feedback.append("Good match. A few improvements can make your resume stand out.")
    elif percentage >= 35:
        feedback.append("Moderate match. Consider tailoring your resume more to this role.")
    else:
        feedback.append("Low match. Significant gaps found between your resume and the JD.")

    if missing_keywords:
        top_missing = sorted(list(missing_keywords))[:15]
        feedback.append(f"Consider adding these keywords: {', '.join(top_missing)}.")

    feedback.append(
        f"You already match {len(common_keywords)} out of {len(jd_keywords_clean)} relevant keywords from the JD."
    )

    return {
        "score": percentage,
        "semantic_score": round(semantic_score * 100, 2),
        "keyword_score": round(keyword_score * 100, 2),
        "common_keywords": sorted(list(common_keywords)),
        "missing_keywords": sorted(list(missing_keywords)),
        "feedback": feedback
    }