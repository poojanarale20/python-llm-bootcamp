from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline

# 1. Load documents from mydata.txt
def load_documents(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        docs = [line.strip() for line in f if line.strip()]
    return docs

# 2. Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Load QA pipeline
qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')

def build_faiss_index(documents):
    doc_embeddings = embedder.encode(documents, convert_to_numpy=True)
    dim = doc_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(doc_embeddings)
    return index, doc_embeddings

def retrieve(query, index, documents, top_k=2):
    query_vec = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, top_k)
    return [(documents[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

def answer_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']

def rag_qa_bot(question, index, documents, top_k=2):
    retrieved = retrieve(question, index, documents, top_k)
    print("\nRetrieved documents:")
    for doc, dist in retrieved:
        print(f"- {doc} (Distance: {dist:.4f})")

    combined_context = " ".join([doc for doc, _ in retrieved])
    answer = answer_question(question, combined_context)
    return answer

if __name__ == "__main__":
    # Load docs from file
    documents = load_documents("mydata.txt")
    print(f"Loaded {len(documents)} documents.")

    # Build FAISS index
    index, _ = build_faiss_index(documents)
    print("FAISS index built.")

    # Interactive Q&A loop
    while True:
        query = input("\nEnter your question (or 'exit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        answer = rag_qa_bot(query, index, documents, top_k=2)
        print(f"\nAnswer: {answer}")
