import os
from pathlib import Path
from .extract_text import extract_text_from_pdf
from .clean_text import clean_text
from .chunk_text import create_chunks

def ingest_all_pdfs(input_folder="data/pdfs", output_folder="data/processed"):

    # Obtener la ruta absoluta del proyecto (dos niveles arriba del archivo)
    project_root = Path(__file__).resolve().parents[2]

    input_path = project_root / input_folder
    output_path = project_root / output_folder

    print("PROJECT ROOT:", project_root)
    print("INPUT PATH:", input_path)

    output_path.mkdir(parents=True, exist_ok=True)

    chunks_all = []
    i = 0

    pdf_files = sorted(input_path.glob("*.pdf"))

    for pdf_file in pdf_files:
        print("Pdf_file:", pdf_file)
        raw   = extract_text_from_pdf(pdf_file)
        clean = clean_text(raw)
        chunks = create_chunks(clean)
        chunks_all.extend([{"text": c, "source": pdf_file.name} for c in chunks])
    return chunks_all



if __name__=="__main__":
    print("REVISION")
    chunks = ingest_all_pdfs(input_folder="data/pdfs",output_folder="data/processed")
    print(chunks)