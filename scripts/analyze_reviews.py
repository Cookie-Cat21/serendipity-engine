import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

# --- One-time setup for NLTK stopwords ---
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
# -----------------------------------------

data_file_path = "data/hotel_reviews.csv"

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# --- Main Analysis Script ---
print(f"Loading the dataset from: {data_file_path}")
df = pd.read_csv(data_file_path)
print("Dataset loaded successfully.")

print("\nCleaning text data...")
df['cleaned_review'] = df['Review'].apply(clean_text)
print("Cleaning complete.")

# --- Sentiment Analysis with a Better Model ---
print("\nInitializing a more suitable Sentiment Analysis model...")
# --- THIS IS THE ONLY LINE WE CHANGED ---
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
print("Model initialized successfully.")

reviews_to_analyze = df['cleaned_review'][:100].tolist()

print("\nAnalyzing sentiment for the first 100 reviews...")
sentiments = sentiment_pipeline(reviews_to_analyze)
print("Analysis complete.")

# Create a temporary DataFrame for our results
results_df = df.iloc[:100].copy()

# This model uses different labels ('LABEL_0', 'LABEL_1', 'LABEL_2')
# We will map them to 'negative', 'neutral', 'positive'
label_mapping = {'LABEL_0': 'negative', 'LABEL_1': 'neutral', 'LABEL_2': 'positive'}
results_df['sentiment_label'] = [label_mapping[s['label']] for s in sentiments]
results_df['sentiment_score'] = [s['score'] for s in sentiments]

print("\n--- Top 10 Results with the NEW Model ---")
# Show the columns we care about
print(results_df[['Rating', 'sentiment_label', 'sentiment_score', 'Review']].head(10))