from prefect import flow, task, get_run_logger
import mlflow

from src.ingestion import fetch_data
from src.preprocessor import preprocess_data
from src.vectorization import bow_vectorizer, word2vec_vectorizer
from src.train import train_models

mlflow.set_tracking_uri("http://localhost:5090")
mlflow.set_experiment("llm project")


@task
def ingest_task(data_path: str):
    logger = get_run_logger()
    logger.info(" Starting data ingestion")
    df = fetch_data(data_path)
    logger.info(" Data ingestion completed")
    return df


@task
def preprocess_task(df):
    logger = get_run_logger()
    logger.info(" Starting preprocessing")
    df = preprocess_data(df)
    logger.info(" Preprocessing completed")
    return df


@task
def vectorize_task(df):
    logger = get_run_logger()
    logger.info(" Starting vectorization")

    X_bow = bow_vectorizer(df["final_cleaned_text"])
    X_cbow = word2vec_vectorizer(df["final_cleaned_text"], sg=0)
    X_skip = word2vec_vectorizer(df["final_cleaned_text"], sg=1)

    logger.info(" Vectorization completed")

    return {
        "BoW": X_bow,
        "Word2Vec-CBOW": X_cbow,
        "Word2Vec-SkipGram": X_skip
    }


@task
def train_task(X, y, vectorizer_name):
    logger = get_run_logger()
    results = train_models(X, y)

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


@flow
def nlp_pipeline(data_path):
    with mlflow.start_run(run_name="Full-Pipeline"):
        df = ingest_task(data_path)
        df = preprocess_task(df)

        y = df["Sentiment"]

        vectorizers = {
            "BoW": bow_vectorizer(df["final_cleaned_text"]),
            "Word2Vec-CBOW": word2vec_vectorizer(df["final_cleaned_text"], sg=0),
            "Word2Vec-SkipGram": word2vec_vectorizer(df["final_cleaned_text"], sg=1),
        }

        for name, X in vectorizers.items():
            train_task(X, y, name)



nlp_pipeline("Dataset/Product_Reviews.csv")