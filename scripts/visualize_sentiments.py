import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- All previous setup and functions ---
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

data_file_path = "data/hotel_reviews.csv"

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# --- Main Visualization Script ---
print("Loading dataset...")
df = pd.read_csv(data_file_path)

print("Cleaning text data...")
df['cleaned_review'] = df['Review'].apply(clean_text)

print("Initializing Sentiment Analysis model...")
# --- THIS IS THE FINAL FIX ---
# We now specify the maximum length for truncation.
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment",
    truncation=True,
    max_length=512 
)

# --- Analyze ALL reviews ---
print("\nAnalyzing sentiment for ALL 20,491 reviews...")
print("This will take a significant amount of time on a CPU. Please be patient and let it run.")
all_reviews = df['cleaned_review'].tolist()
sentiments = sentiment_pipeline(all_reviews)
print("Analysis complete!")

# --- Add results to DataFrame ---
label_mapping = {'LABEL_0': 'negative', 'LABEL_1': 'neutral', 'LABEL_2': 'positive'}
df['sentiment_label'] = [label_mapping[s['label']] for s in sentiments]
df['sentiment_score'] = [s['score'] for s in sentiments]

# --- Visualization ---
print("\nGenerating sentiment distribution chart...")
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.countplot(
    x='sentiment_label',
    data=df,
    palette=['#CC0000', '#FFBB02', '#008009'],
    order=['negative', 'neutral', 'positive']
)
ax.set_title('Distribution of Review Sentiments', fontsize=16)
ax.set_xlabel('Sentiment', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)

# Ensure the 'output' directory exists
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

chart_path = os.path.join(output_folder, "sentiment_distribution.png")
plt.savefig(chart_path)

print(f"\nSuccess! Chart saved to '{chart_path}'")