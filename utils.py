def classify_intent(llm, message, chat_history):
    """Classify the user's intent based on the message and chat history."""
    prompt = (
        "Given the following chat history and the latest user message, "
        "classify the user's intent as one of: 'add_memory', 'retrieve_memory', or 'delete_memory'. "
        "Respond with only the intent string.\n\n"
        f"Chat history: {chat_history}\n"
        f"Message: {message}"
    )
    response = llm.invoke(prompt)
    return response.content.strip()


def extract_facts(llm, message):
    """Extract facts from the user's message using the LLM."""
    prompt = (
        "You are an assistant that extracts clear, distinct facts from user messages for long-term memory storage. "
        "A fact should be a simple, atomic statement about the user's preferences, actions, events, relationships, or anything else. "
        "Return ONLY a valid Python list of strings, with each string being a single fact. "
        "If there are no facts, return an empty list ([]).\n"
        f"Message: {message}"
    )
    response = llm.invoke(prompt)
    content = response.content.strip()
    try:
        facts_list = eval(content)
        if isinstance(facts_list, list):
            return facts_list
        else:
            return []
    except Exception as e:
        print(f"Error parsing facts: {e}")
        return []
    
def get_chat_history(memory):
    """Returns a string representation of the chat history"""
    history = memory.load_memory_variables({})["chat_history"]
    if isinstance(history, list):
        return "\n".join([f"{m.type.capitalize()}: {m.content}" for m in history])
    return history