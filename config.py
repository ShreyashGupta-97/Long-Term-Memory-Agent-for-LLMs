import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory

# ---- Load API Key securely ----
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

# Initialize shared models and vectorstore here
llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

# Persistent local storage directory
PERSIST_DIRECTORY = "./chroma_db"

def get_vectorstore(user_id="default"):
    return Chroma(
        collection_name=f"memories_{user_id}",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )

def get_memory():
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)