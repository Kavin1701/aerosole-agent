import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

env_path = Path(__file__).resolve().parents[4] / "config" / "langgraph_agent.env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class VectorRetriever:

    def __init__(self, vector_store_dir="vector_retriever_model/faiss_index"):
        self.vector_store_dir = Path(__file__).resolve().parent / vector_store_dir
        self.vector_store = self.get_vector_store()

    def get_embedder(self):
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=OPENAI_API_KEY
        )

    def get_vector_store(self):
        embedder = self.get_embedder()
        return FAISS.load_local(
            folder_path=self.vector_store_dir,
            embeddings=embedder,
            allow_dangerous_deserialization=True
        )
    
    def __call__(self, query, top_k=5, confidence_threshold=40):
        results = self.vector_store.similarity_search_with_score(query, k=top_k)

        response = []
        for doc, distance in results:
            # Convert L2 → cosine similarity approximation
            l2_squared = distance ** 2
            cosine_similarity = 1 - (l2_squared / 2)
            similarity = max(0.0, cosine_similarity)

            confidence = round(similarity * 100, 2)

            # Filter out low confidence matches
            if confidence >= confidence_threshold:
                response.append({
                    "title": doc.metadata.get("id"),
                    "content": doc.page_content,
                    "distance": round(float(distance), 4),
                    "similarity": round(similarity, 4),
                    "confidence": confidence
                })

        return response
