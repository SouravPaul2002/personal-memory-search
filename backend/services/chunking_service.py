def chunk_text(text, chunk_size=500, overlap=50):
    """
    Word-based chunking with overlap.
    More accurate than character chunking.
    """

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if len(chunk.strip()) > 100:
            chunks.append(chunk)

    return chunks