from config import llm, embeddings, get_vectorstore, get_memory
from utils import classify_intent, extract_facts, get_chat_history
from vectorstore_utils import add_memory_to_vectorstore, delete_memory_from_vectorstore, retrieve_memory

def main():
    print("Conversational Memory Agent (type 'exit' to quit)")
    vectorstore = get_vectorstore(user_id="default")
    memory = get_memory()

    while True:
        user_message = input("\nYou: ")
        if user_message.strip().lower() == "exit":
            break

        # Add user message to memory
        memory.save_context({"input": user_message}, {"output": ""})

        chat_history = get_chat_history(memory)
        intent = classify_intent(llm, user_message, chat_history)
        intent = intent.strip().strip('"').strip("'").rstrip(".").lower()

        if intent == "add_memory":
            facts_to_add = extract_facts(llm, user_message)
            add_memory_to_vectorstore(vectorstore, facts_to_add)
            agent_reply = "Updated the memory accordingly."

        elif intent == "delete_memory":
            facts_to_delete = extract_facts(llm, user_message)
            if facts_to_delete:
                delete_memory_from_vectorstore(vectorstore, facts_to_delete)
                agent_reply = f"Task completed as per your request."
            else:
                agent_reply = "No deletion detected."

        elif intent == "retrieve_memory":
            agent_reply = retrieve_memory(vectorstore, user_message)
        else:
            agent_reply = "Sorry, I couldn't understand your intent."

        print("Agent:", agent_reply)

        # Add agent reply to memory
        memory.save_context({"input": ""}, {"output": agent_reply})

if __name__ == "__main__":
    main()