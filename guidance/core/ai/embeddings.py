
from fastembed import TextEmbedding

MODEL_CACHE = "/app/model_cache"

embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_dir=MODEL_CACHE,
)
