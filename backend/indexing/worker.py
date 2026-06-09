from backend.indexing.job_queue import (
    index_queue
)

from backend.indexing.pdf_indexer import (
    index_pdf
)

from backend.indexing.image_indexer import (
    index_image
)


def process_jobs():

    completed_jobs = []

    while not index_queue.empty():

        job = index_queue.get()

        print(
            f"Processing: {job['filename']}"
        )

        result = None

        if job["type"] == "pdf":

            result = index_pdf(
                pdf_path=job["pdf_path"],
                filename=job["filename"]
            )

        elif job["type"] == "image":

            result = index_image(
                image_path=job["image_path"],
                filename=job["filename"]
            )

        if result:

            job["result"] = result

            completed_jobs.append(
                job
            )

        index_queue.task_done()

    return completed_jobs