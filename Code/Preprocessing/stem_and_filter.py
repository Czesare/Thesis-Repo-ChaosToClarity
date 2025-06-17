import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# === STOPWORD CONFIGURATION ===

# Default Dutch stopwords from NLTK
default_stop_words = set(stopwords.words('dutch'))

# Optional: add or remove domain-specific stopwords
# You can include or exclude negations like "niet" and "geen" depending on your model's needs
# If negation is important for classification (e.g., "niet goed"), consider removing them from the list below
custom_stop_words = default_stop_words | {
    '<email>', '<datum>', '<phone>', '<postalcode>', 'dtx',
    '<<email>>',
    'niet',  # <-- REMOVE this if you want to keep negation
    'geen'   # <-- REMOVE this if you want to keep negation
}


# === STEMMING FUNCTION ===

stemmer = SnowballStemmer('dutch')

def preprocess_text(text: str) -> str:
    """
    Applies stopword removal and stemming to a given text.
    """
    words = text.split()
    cleaned_words = [stemmer.stem(word) for word in words if word.lower() not in custom_stop_words]
    return ' '.join(cleaned_words)


# === FILE PROCESSING ===

def process_file(input_file: str, output_file: str):
    """
    Reads a CSV file, applies stemming + stopword removal on the 'combined_text' column,
    and writes the cleaned output to a new CSV file.
    """
    try:
        print(f"Loading: {input_file}")
        df = pd.read_csv(input_file, delimiter=';')
        print("Applying text preprocessing...")

        df['combined_text'] = df['combined_text'].astype(str).apply(preprocess_text)

        print(f"Saving to: {output_file}")
        df.to_csv(output_file, index=False, encoding='utf-8')
        print("Done.")
    except Exception as e:
        print(f"[ERROR] {e}")


# === ENTRY POINT (SAFE TO REMOVE FOR IMPORTING IN PIPELINES) ===

if __name__ == "__main__":
    input_path = "<INPUT_PATH>.csv"       # e.g. "data/raw_dataset.csv"
    output_path = "<OUTPUT_PATH>.csv"     # e.g. "data/cleaned_dataset.csv"
    process_file(input_path, output_path)
