# pyrefly: ignore [missing-import]
import open_clip
# pyrefly: ignore [missing-import]
import torch

from PIL import Image


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


def generate_image_embedding(
    image_path
):

    image = preprocess(
        Image.open(
            image_path
        )
    ).unsqueeze(0)

    with torch.no_grad():

        embedding = model.encode_image(
            image
        )

        embedding /= embedding.norm(
            dim=-1,
            keepdim=True
        )

    return embedding[0].tolist()


def generate_text_embedding(
    text
):

    tokens = tokenizer(
        [text]
    )

    with torch.no_grad():

        embedding = model.encode_text(
            tokens
        )

        embedding /= embedding.norm(
            dim=-1,
            keepdim=True
        )

    return embedding[0].tolist()