import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

class TfidfRetriever:
    def __init__(
        self,
        df: pd.DataFrame = None,
        force_recreate=False,
        artifact_dir=None,
        max_features=5000
    ):
        """
        If TF-IDF artifacts exist and force_recreate=False → load them.
        Otherwise → require df and build from scratch.
        """

        # -------------------------
        # FIXED: Setup artifact dir
        # -------------------------
        if artifact_dir:
            self.artifact_dir = Path(artifact_dir)
        else:
            self.artifact_dir = Path(__file__).resolve().parent

        # Create root artifact folder
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

        # ✅ Create the SUBFOLDER before using it
        self.model_dir = self.artifact_dir / "tfidf_retriever_model"
        self.model_dir.mkdir(parents=True, exist_ok=True)

        # Artifact paths
        self.vectorizer_path = self.model_dir / "tfidf_vectorizer.pkl"
        self.matrix_path = self.model_dir / "tfidf_matrix.pkl"
        self.titles_path = self.model_dir / "tfidf_metadata.pkl"

        self.max_features = max_features

        # Check artifacts
        artifacts_exist = (
            self.vectorizer_path.exists() and
            self.matrix_path.exists() and
            self.titles_path.exists()
        )

        if artifacts_exist and not force_recreate:
            print("🔹 Existing TF-IDF artifacts found. Loading retriever...")
            self._load()
        else:
            if df is None:
                raise ValueError("❌ df must be provided when creating a new retriever.")

            print("🔹 Building a NEW TF-IDF retriever...")
            self.df = df.reset_index(drop=True)
            self._build(self.df)
            self._save()

    # -------------------------------------------------------------
    # 1) Build TF-IDF model
    # -------------------------------------------------------------
    def _build(self, df: pd.DataFrame):
        # STEP 1: Prepare text
        df["combined_text"] = (
            df["title"].fillna("") + " " +
            df["subtitle"].fillna("") + " " +
            df["short_description"].fillna("") + " " +
            df["style_description"].fillna("") + " " +
            df["details"].fillna("")
        )
        print("1) Combined text created. Example:")
        print("   ", df['combined_text'].iloc[0][:200], "...")
        print()

        # STEP 2: Create and fit vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
            max_features=self.max_features
        )
        print(f"2) Vectorizer initialized (max_features={self.max_features})")

        self.tfidf_matrix = self.vectorizer.fit_transform(df["combined_text"])
        print("2.1) TF-IDF matrix shape:", self.tfidf_matrix.shape)
        print()

        # STEP 3: Feature checks
        self.features = self.vectorizer.get_feature_names_out()
        print("3) Vocabulary Size:", len(self.features))
        print("   First 15 features:", self.features[:15])
        print()

    # -------------------------------------------------------------
    # 2) Save artifacts
    # -------------------------------------------------------------
    def _save(self):
        # Save vectorizer
        with open(self.vectorizer_path, "wb") as f:
            pickle.dump(self.vectorizer, f)

        # Save matrix
        with open(self.matrix_path, "wb") as f:
            pickle.dump(self.tfidf_matrix, f)

        # Save ONLY titles
        self.df[["title"]].to_pickle(self.titles_path)

        print("6) Saved TF-IDF artifacts:")
        print("   -", self.vectorizer_path)
        print("   -", self.matrix_path)
        print("   -", self.titles_path)
        print()

    # -------------------------------------------------------------
    # 3) Load artifacts
    # -------------------------------------------------------------
    def _load(self):
        with open(self.vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)

        with open(self.matrix_path, "rb") as f:
            self.tfidf_matrix = pickle.load(f)

        self.df = pd.read_pickle(self.titles_path)

        self.features = self.vectorizer.get_feature_names_out()

        print("Loaded retriever:")
        print("   - vocab size:", len(self.features))
        print("   - matrix shape:", self.tfidf_matrix.shape)
        print("   - titles loaded:", len(self.df))
        print()

    # -------------------------------------------------------------
    # 4) Retrieve top-k results using cosine similarity
    # -------------------------------------------------------------
    def __call__(self, query, top_k=5):
        print("🔎 Retrieving for query:", query)

        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()

        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "title": self.df.iloc[idx]["title"],
                "score": float(scores[idx]),
            })

        return results
