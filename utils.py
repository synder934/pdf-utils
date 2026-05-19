from pypdf import PdfReader, PdfWriter
from pathlib import Path
import subprocess


def any2pdf_linux(doc: Path, output_dir: Path):
    cmd = ["libreoffice", "--convert-to", "pdf", str(doc), "--outdir", str(output_dir)]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=10)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)


def compile_pdfs(paths):
    writer = PdfWriter()

    try:
        for path in paths:
            pdf = PdfReader(path)
            writer.append(pdf)

        return writer
    except Exception as e:
        print(path)
        raise e


if __name__ == "__main__":
    test_file = Path("inputs") / "COM2041-lectures" / "COM2041_lecture 9 2026-full.pptx"
    # print(test_file.)
    raise Exception()
    any2pdf_linux(test_file, test_file.parent)
