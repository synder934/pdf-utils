import os
from pathlib import Path
from utils import compile_pdfs, any2pdf_linux
import logging

pypdf_logger = logging.getLogger("pypdf")
pypdf_logger.setLevel(logging.ERROR)

FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] -on line: %(lineno)d - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(FORMATTER)
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    input_dir = Path("inputs")
    output_dir = Path("outputs")

    try:
        os.mkdir(input_dir)
    except:
        pass

    try:
        os.mkdir(output_dir)
    except:
        pass

    completed = set()
    for file in os.listdir(output_dir):
        name = file.split(".")[0]
        completed.add(name)

    logger.debug(f"completed files: {completed}")

    for folder in os.listdir(input_dir):
        if folder in completed:
            logger.warning(f"Already exists: {folder}.pdf")
            continue

        logger.info(f"Creating: {folder}.pdf ...")

        for file in sorted(os.listdir(input_dir / folder)):
            if file.split(".")[-1] != "pdf":
                logger.debug(f"Converting {file} to pdf ...")

                path = input_dir / folder / file
                any2pdf_linux(path, path.parent)

                logger.debug(f"Converted {file} to pdf.")

        logger.debug(f"Compiling: {folder} ...")
        writer = compile_pdfs(
            [
                input_dir / folder / file
                for file in os.listdir(input_dir / folder)
                if file.split(".")[-1] == "pdf"
            ]
        )
        logger.debug(f"Compiled: {folder}.")

        with open(output_dir / f"{folder}.pdf", "bw+") as f:
            writer.write(f)

        logger.info(f"Created: {folder}.pdf")
