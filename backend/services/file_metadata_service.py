import mimetypes


def get_mime_type(
    file_path
):

    mime_type, _ = mimetypes.guess_type(
        file_path
    )

    return mime_type or "unknown"