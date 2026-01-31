from prefect import flow, task, get_run_logger
import mlflow
from src.ingestion import fetch_data
from src.preprocessor import preprocess_data, preprocess_single_text
from src.vectorization import bow_vectorizer, word2vec_vectorizer
from src.train import train_models

mlflow.set_tracking_uri("http://localhost:5090")
mlflow.set_experiment("llm project")


@task
def ingest_task(data_path: str):
    logger = get_run_logger()
    logger.info("Starting data ingestion")
    df = fetch_data(data_path)
    logger.info("Data ingestion completed")
    return df


@task
def preprocess_task(df):
    logger = get_run_logger()
    logger.info("Starting preprocessing")
    df = preprocess_data(df)
    logger.info("Preprocessing completed")
    return df


@task
def train_task(X, y, vectorizer_name):
    logger = get_run_logger()
    results = train_models(X, y)

    best_model = None
    best_f1 = -1

    for model_name, f1, model, *_ in results:
        with mlflow.start_run(nested=True):
            logger.info(f"Logging {model_name} | {vectorizer_name}")

            mlflow.log_param("vectorizer", vectorizer_name)
            mlflow.log_param("model", model_name)
            mlflow.log_metric("macro_f1", f1)

            mlflow.sklearn.log_model(
                model,
                artifact_path=f"{vectorizer_name}/{model_name}"
            )

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

    return best_model, best_f1


@flow
def nlp_pipeline(data_path="Dataset/Product_Reviews.csv"):
    """Full training pipeline that returns the best model and its vectorizer"""
    df = ingest_task(data_path)
    df = preprocess_task(df)
    y = df["Sentiment"]

    # Create vectorizers
    vectorizers = {
        "BoW": bow_vectorizer(df["final_cleaned_text"]),
        "Word2Vec-CBOW": word2vec_vectorizer(df["final_cleaned_text"], sg=0),
        "Word2Vec-SkipGram": word2vec_vectorizer(df["final_cleaned_text"], sg=1),
    }

    best_model_overall = None
    best_vectorizer_name = None
    best_vectorizer_X = None
    best_f1 = -1

    for name, X in vectorizers.items():
        model, f1 = train_task(X, y, name)
        if f1 > best_f1:
            best_f1 = f1
            best_model_overall = model
            best_vectorizer_name = name
            best_vectorizer_X = X

    return best_model_overall, best_vectorizer_name, best_vectorizer_X


def predict_sentiment(news_text: str, model, vectorizer_name, vectorizer_X):
    """Predict sentiment for a single news text"""
    cleaned_text = preprocess_single_text(news_text)

    # Transform input according to vectorizer used
    if vectorizer_name == "BoW":
        X_new = bow_vectorizer([cleaned_text])
    else:
        sg = 0 if vectorizer_name == "Word2Vec-CBOW" else 1
        X_new = word2vec_vectorizer([cleaned_text], sg=sg)

    prediction = model.predict(X_new)[0]
    return prediction
