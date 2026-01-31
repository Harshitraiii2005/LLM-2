import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    text = text.lower().strip()
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna().drop_duplicates()
    df["final_cleaned_text"] = df["Product Review"].apply(clean_text)
    return df

def preprocess_single_text(text: str) -> str:
    """
    Preprocess a single input string for inference/prediction.
    This should NEVER use pandas operations.
    """
    if not isinstance(text, str):
        raise ValueError("Input to preprocess_single_text must be a string")

    text = text.strip()
    if text == "":
        return ""

    return clean_text(text)
