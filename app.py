# Importación de módulos
import openai  # Importa el módulo openai para interactuar con la API de OpenAI.
import os  # Importa el módulo os para manipular variables de entorno y el sistema operativo.
from flask import Flask, render_template, request, jsonify  # Importa clases y funciones desde el módulo flask para crear una aplicación web.
from cachetools import LRUCache  # Importa la clase LRUCache desde cachetools para implementar una caché de tamaño limitado.
from langchain.chains import ConversationalRetrievalChain  # Importa una clase para la cadena de recuperación conversacional.
from langchain.chat_models import ChatOpenAI  # Importa una clase para el modelo de chat basado en OpenAI.
from langchain.document_loaders import DirectoryLoader  # Importa una clase para cargar documentos desde un directorio.
from langchain.indexes import VectorstoreIndexCreator  # Importa una clase para crear un índice utilizando Vectorstore.
import chromadb  # Importa el módulo chromadb para interactuar con la base de datos ChromaDB.
from chromadb.config import Settings  # Importa la clase Settings desde chromadb.config para configurar ChromaDB.
import constants  # Importa un módulo personalizado llamado constants para acceder a una clave API y otras constantes.
import uuid  # Importa el módulo uuid para generar identificadores únicos.
import tiktoken  # Importa el módulo tiktoken para trabajar con tokens.

encoding = constants.ENCODING_NAME
encodingModel = constants.ENCODING_MODEL

# Establece la clave de la API de OpenAI usando el valor definido en constants.APIKEY.
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Creación de la aplicación Flask
app = Flask(__name__)  # Crea una instancia de la clase Flask con el nombre del módulo actual.

# Configura la carpeta estática para servir archivos estáticos
app.static_folder = 'static'  # Establece la carpeta 'static' como la carpeta para archivos estáticos.

# Carga los documentos desde el directorio "TemporaryVisas/"
loader = DirectoryLoader("TemporaryVisas/")  # Crea una instancia de DirectoryLoader para cargar documentos desde el directorio "TemporaryVisas/".

# Crea un nuevo índice utilizando VectorstoreIndexCreator y los datos cargados desde loader.
index = VectorstoreIndexCreator().from_loaders([loader])  # Crea un índice utilizando VectorstoreIndexCreator y los datos de carga de loader.

# Creación de una cadena de recuperación conversacional
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),  # Crea una cadena de recuperación conversacional con un modelo ChatOpenAI específico.
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),  # Configura el retriever con opciones de búsqueda.
)

# Agrega un caché para las respuestas
response_cache = LRUCache(maxsize=100)  # Crea una caché LRUCache con un tamaño máximo de 100 elementos.

# Historial de la conversación
chat_history = []  # Inicializa una lista para almacenar el historial de la conversación.

# #Generación de un cliente persistente
chroma_client = chromadb.PersistentClient(path="/home/chatgpt-demo/ChatGPT/ChGPT_Chroma")

# chroma_client = chromadb.Client(
#     Settings(chroma_db_impl="duckdb+parquet",  # Configura el cliente ChromaDB con la implementación y opciones de almacenamiento.
#              persist_directory="C:/Users/DULCE/Documents/Tec Saltillo/TXM/ChatGPTChroma")  # Establece el directorio de persistencia.
# )

# Buscar la colección en ChromaDB
collection_name = "my_collection"
collection = chroma_client.get_collection(name=collection_name)  # Busca la colección en ChromaDB con el nombre "my_collection".
if collection is None:
#     Si la colección no existe, se crea una nueva.
    collection = chroma_client.create_collection(name=collection_name)  # Crea una colección en ChromaDB con el nombre "my_collection".

def num_tokens_from_string(response: str, encoding_name: str, type_response: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)

    if(type_response == "incoming"):
        #print(response,"\n")
        message =[{
            "role": "user",
            "content": response,
        }]

        tokens_per_message = 4 
        # every message follows <|start|>{role/name}n{content}<|end|>n

        num_tokens = 0
        num_tokens += tokens_per_message

        for key, value in message[0].items():
            response=value
            num_tokens+=len(encoding.encode(value))
            #print(f"{len(encoding.encode(value))} is the number of token included in {key}")

        num_tokens += 3
        # every reply is primed with <|start|>assistant<|message|>

        #print(f"{num_tokens} number of tokens to be sent in our request")
    elif(type_response == "outcoming"):
        #print(response, "\n")
        num_tokens = len(encoding.encode(response))
        print(f"{num_tokens} number of tokens from our answer (by tiktoken)")
    return num_tokens

# Define la solicitud inicial (prompt)
prompt = "Por favor, proporciona un resumen conciso sobre la información de las visas de Estados Unidos en forma de párrafo en viñetas."

def get_chatbot_response(user_input):
    # Agrega el prompt como la primera pregunta en el historial de conversación
    chat_history.append((prompt, ""))  # El segundo elemento en la tupla se deja en blanco inicialmente.

    if user_input in response_cache:  # Comprueba si la respuesta está en la caché.
        return {
            "response": response_cache[user_input],
            "num_tokens_used": 0,  # Puedes ajustar esto según tus necesidades.
            "saldo_inicial_de_tokens": 0,  # Puedes ajustar esto según tus necesidades.
            "restante": 0,  # Puedes ajustar esto según tus necesidades.
            "gastado": 0  # Puedes ajustar esto según tus necesidades.
        }  # Devuelve la respuesta desde la caché si está presente.
    
    incoming_tokens = num_tokens_from_string(user_input, encodingModel, "incoming")
    print("Incoming tokens Model: ", incoming_tokens, "\n")

    response = chain({"question": user_input, "chat_history": chat_history, "temperature": 0.5})['answer']
    response = response.replace("\n", "<br>")  # Replace newline characters with HTML line breaks
    response_cache[user_input] = response  # Almacena la respuesta en la caché.
    
    # message =[{
    #      "role": "user",
    #      "content": user_input,
    #  }]
        
    # responseOpenAI = openai.ChatCompletion.create(
    #      model='gpt-3.5-turbo-0301',
    #      messages=message,
    #      temperature=0,
    #      max_tokens=500
    # )

    #print(responseOpenAI)
    outcoming_tokens =  num_tokens_from_string(response, encodingModel, "outcoming")
    print("Outcoming tokens Model: ", outcoming_tokens)

    #content = response["choices"][0]["message"]["content"]

    # response = chain({"question": user_input, "chat_history": chat_history})['answer']
    # response = response.replace("\n", "<br>")  # Replace newline characters with HTML line breaks
    # #response_cache[user_input] = content # Almacena la respuesta en la caché.
    # response_cache[user_input] = response  # Almacena la respuesta en la caché.

    # Agrega la pregunta y la respuesta a la colección de ChromaDB
    collection.add(documents=[user_input, response], ids=[str(uuid.uuid4()), str(uuid.uuid4())])  # Agrega la pregunta y respuesta a ChromaDB.

    # Saldo de Tokens
    saldo_inicial_de_tokens = 5833333

    # Nombre del archivo de texto
    nombre_archivo = "mi_archivo.txt"

    # Abrir el archivo en modo de lectura ('r')
    with open(nombre_archivo, 'r') as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()

    # El archivo se cierra automáticamente al salir del bloque 'with'

    saldo_de_tokens = int(contenido)

    #restante = saldo_de_tokens - incoming_tokens

    restante = saldo_de_tokens - ( incoming_tokens + outcoming_tokens )
    gastado = saldo_inicial_de_tokens - restante
    
    # Print the number of tokens used
    print(f"Número de tokens totales: {saldo_inicial_de_tokens}")
    print(f"Número de tokens restantes: {restante}")
    print(f"Número de tokens usados: {incoming_tokens + outcoming_tokens}")
    print(f"Número de tokens gastados: {gastado}")

    # Valor que deseas almacenar (converted to a string)
    valor = str(restante)

    # Nombre del archivo de texto
    nombre_archivo = "mi_archivo.txt"

    # Escribe el valor en el archivo (reemplazando el contenido existente)
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(valor + '\n')

    return {
        "response": response,
        "num_tokens_used": incoming_tokens,
        "saldo_inicial_de_tokens": saldo_inicial_de_tokens,
        "restante": restante,
        "gastado": gastado

    }  # Devuelve la respuesta obtenida.

# Configuración de la ruta de inicio de la aplicación web
@app.route("/")
def index():
    return render_template("index.html", initial_prompt=prompt)  # Renderiza / convierte el template "index.html" al acceder a la ruta raíz.

# Ruta para obtener respuestas del chatbot
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    response_data = get_chatbot_response(user_input)
    chat_history.append((user_input, response_data["response"]))
    return jsonify(response_data)

# Inicio de la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)  # Inicia la aplicación Flask en modo de depuración.