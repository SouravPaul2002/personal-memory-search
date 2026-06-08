import open_clip
import torch

from PIL import Image

print("Loading model...")

model, _, preprocess = (
    open_clip.create_model_and_transforms(
        "ViT-B-32",
        pretrained="laion400m_e32"
    )
)

tokenizer = open_clip.get_tokenizer(
    "ViT-B-32"
)

model.eval()

print("Model loaded!")

image = preprocess(
    Image.open(
        "data/images/red-ballpoint-pen.jpeg"
    )
).unsqueeze(0)

text = tokenizer([
    "red pen",
    "blue car",
    "python code",
    "cat",
    "bicycle"
])

with torch.no_grad():

    image_features = model.encode_image(
        image
    )

    text_features = model.encode_text(
        text
    )

    image_features /= image_features.norm(
        dim=-1,
        keepdim=True
    )

    text_features /= text_features.norm(
        dim=-1,
        keepdim=True
    )

    similarity = (
        image_features @ text_features.T
    )

print("\nSimilarity Scores:\n")

for label, score in zip(
    [
        "red pen",
        "blue car",
        "python code",
        "cat",
        "bicycle"
    ],
    similarity[0]
):
    print(
        f"{label}: {score.item():.4f}"
    )