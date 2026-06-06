from sentence_transformers import SentenceTransformer

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def generate_embedding(text):
    return model.encode(text).tolist()

# Multiple embedding in one call 
def generate_embeddings(texts):
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    ).tolist()