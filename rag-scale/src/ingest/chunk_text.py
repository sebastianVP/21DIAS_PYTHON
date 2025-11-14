from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(text, chunk_size=1000, overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_text(text)