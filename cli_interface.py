import os
import sys
from chatgpt import ConversationalRetrievalChain, ChatOpenAI, VectorstoreIndexCreator, DirectoryLoader, OpenAIEmbeddings, VectorStoreIndexWrapper
import constants

# Set the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

# Check if persistence is enabled and if an index already exists on disk
if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    # Load vectorstore from persistence
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
    loader = DirectoryLoader("TemporaryVisas/")
    if PERSIST:
        # Create index and save to disk
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        # Create index without saving to disk
        index = VectorstoreIndexCreator().from_loaders([loader])

# Create a conversational retrieval chain using the ChatOpenAI model and the index
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
while True:
    query = input("Enter your question (or 'q' to quit): ")
    if query.lower() in ['quit', 'q', 'exit']:
        sys.exit()  # Exit the program if the query is one of the exit commands
    
    result = chain({"question": query, "chat_history": chat_history})
    print("Answer:", result['answer'])  # Print the answer from the retrieval chain

    chat_history.append((query, result['answer']))  # Add query and answer to chat history
