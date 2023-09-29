# Import necessary libraries and modules
import os
import sys
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import constants

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Function to fetch and extract content from a URL and its subpages
#def extract_content_from_url(url, max_depth=2):
#    try:
#        response = requests.get(url)
#        response.raise_for_status()
#        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the webpage
#        content = soup.get_text()
        # Save the webpage content to a file in the data directory
#        with open(f"data/{url.strip('/').replace('/', '_')}.txt", "w", encoding="utf-8") as f:
#            f.write(content)

        # Extract links from the webpage and follow them to fetch content from subpages
#        if max_depth > 0:
#            links = soup.find_all('a')
#            for link in links:
#                subpage_url = link.get('href')
#                if subpage_url and not subpage_url.startswith('#') and not subpage_url.startswith('javascript:'):
#                    if not subpage_url.startswith('http'):  # Handle relative URLs
#                        subpage_url = f"{url.rstrip('/')}/{subpage_url.lstrip('/')}"
#                    extract_content_from_url(subpage_url, max_depth - 1)
#    except requests.exceptions.RequestException as e:
#        print(f"Error fetching URL: {e}")
    

# Add the URL of the webpage you want to scrape here
#webpage_url = "https://ais.usvisa-info.com/"

# Fetch and extract content from the webpage and its subpages (up to depth 2)
#extract_content_from_url(webpage_url, max_depth=2)

# Fetch and extract content from the webpage
#webpage_content = extract_content_from_url(webpage_url)

# Check if the content was successfully extracted, and add it to the DirectoryLoader
#if webpage_content:
    # Save the webpage content to a file in the data directory
#    with open("data/webpage.txt", "w", encoding="utf-8") as f:
#        f.write(webpage_content)     


# Set the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

# Check if a query is provided as a command line argument
query = None
if len(sys.argv) > 1:
    query = sys.argv[1]

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
    if not query:
        query = input("")  # Prompt user for a query if not provided as a command line argument
    if query in ['quit', 'q', 'exit']:
        sys.exit()  # Exit the program if the query is one of the exit commands
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])  # Print the answer from the retrieval chain

    chat_history.append((query, result['answer']))  # Add query and answer to chat history
    query = None  # Reset the query to prompt for the next input