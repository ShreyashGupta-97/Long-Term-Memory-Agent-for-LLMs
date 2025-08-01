from langchain_community.utils.math import cosine_similarity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Initialize shared models and vectorstore here
llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

def add_memory_to_vectorstore(vectorstore, facts_list, similarity_threshold=0.9):
    """Add a list of facts to the vectorstore, avoiding duplicates based on semantic similarity."""
    if not facts_list:
        print("No facts found to add.")
    else:
        for fact in facts_list:
            docs = vectorstore.similarity_search(fact, k=1)
            if docs:
                existing_fact = docs[0].page_content
                fact_embedding = embeddings.embed_query(fact)
                existing_fact_embedding = embeddings.embed_query(existing_fact)
                sim = cosine_similarity([fact_embedding], [existing_fact_embedding])[0][0]
                if sim >= similarity_threshold:
                    print(f"Agent: Fact '{fact}' is too similar to existing fact '{existing_fact}'. Skipping.")
                    continue
            vectorstore.add_texts([fact], ids=[str(hash(fact))])

def delete_memory_from_vectorstore(vectorstore, facts_list):
    """Delete all memories from the vectorstore that match any fact in facts_list. Take confirmation from the user before deleting."""
    for fact in facts_list:
        docs = vectorstore.similarity_search(fact, k=1)
        if not docs:
            print(f"No matching fact found for deletion: {fact}")
        for doc in docs:
            doc_id = getattr(doc, 'id', None) or str(hash(doc.page_content))
            print(f"Agent: I am Deleting fact: '{doc.page_content}. Shall I go ahead? (Y/N)")
            user_message = input("You: ")
            if user_message.strip().lower() == 'y':
                vectorstore.delete(doc_id)
                print(f"Agent: Memory Deleted.")
            else:
                print(f"Agent: Deletion Cancelled.")

def retrieve_memory(vectorstore, query):
    """Retrieve facts from the vectorstore based on a query."""
    docs = vectorstore.similarity_search(query, k=3)
    facts_list = [doc.page_content for doc in docs]
    if not facts_list:
        return "No relevant memories found."
    facts_text = "; ".join(facts_list)
    prompt = (
        f"Given the following facts from the user's memory:\n"
        f"{facts_text}\n\n"
        f"And the user's question: \"{query}\"\n"
        f"Generate a concise, natural language answer to the question using the facts."
    )
    response = llm.invoke(prompt)
    return response.content.strip()