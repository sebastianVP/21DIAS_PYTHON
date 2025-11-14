"""
2.1 Crear embeddings con sentence-transformers
2.2 Crear colección en Qdrant con índice HNSW
2.3 Insertar los vectores
"""
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams,PointStruct,HnswConfigDiff
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "El radar mide la reflectividad de las precipitaciones.",
    "La ionosfera afecta las señales GPS.",
    "El modelo LSTM se usa para series temporales.",
    "Qdrant permite búsquedas semánticas rápidas."
]

texts2 = [
    "Los sistemas de análisis atmosférico combinan observaciones y modelos numéricos para describir el estado de la atmósfera.",
    "ERA5 del ECMWF es uno de los reanálisis más usados por su alta resolución temporal y espacial.",
    "MERRA-2 de la NASA integra datos observacionales y modelados desde 1980 para estudios climáticos.",
    "WRF es un modelo regional utilizado para simulaciones y pronósticos meteorológicos de alta resolución.",
    "GFS es el modelo global de NOAA que proporciona condiciones iniciales para modelos regionales.",
    "Los satélites GOES, Himawari y Meteosat ofrecen imágenes multiespectrales en tiempo casi real.",
    "MODIS, VIIRS y Sentinel permiten analizar aerosoles, temperatura y propiedades de nubes desde órbita polar.",
    "Los radares meteorológicos miden reflectividad y velocidad Doppler para estimar la estructura de las precipitaciones.",
    "Las estaciones automáticas registran variables como temperatura, humedad, presión y precipitación a nivel de superficie.",
    "Herramientas como Py-ART, xarray y MetPy permiten procesar y visualizar datos meteorológicos en Python.",
    "Google Earth Engine facilita el análisis de datos satelitales y climáticos en la nube con alto rendimiento.",
    "BigQuery y Vertex AI en Google Cloud permiten combinar análisis atmosférico con modelos de inteligencia artificial.",
    "Los formatos más comunes para datos atmosféricos son NetCDF, GRIB y HDF5.",
    "El lenguaje Python, junto con librerías como numpy, pandas, cartopy y matplotlib, es clave en el análisis atmosférico moderno.",
    "Los modelos de IA como LSTM o redes convolucionales pueden aplicarse para predecir variables meteorológicas o detectar eventos atmosféricos.",
    "El barómetro se utiliza para medir la presión atmosférica.",
    "Los termómetros miden la temperatura del aire, uno de los parámetros básicos del estado atmosférico.",
    "El higrómetro se usa para medir la humedad relativa del aire.",
    "El anemómetro permite medir la velocidad del viento en superficie o en diferentes alturas.",
    "El pluviómetro se utiliza para medir la cantidad de precipitación acumulada.",
    "El radiosondeo consiste en un globo que lleva sensores para medir presión, temperatura, humedad y viento en la atmósfera.",
    "Los radares meteorológicos miden la reflectividad de las precipitaciones y permiten estimar la intensidad de la lluvia.",
    "Los satélites meteorológicos observan la atmósfera desde el espacio, midiendo temperatura, nubosidad y radiación.",
    "El lidar atmosférico utiliza pulsos de luz láser para medir partículas, aerosoles y perfiles de viento.",
    "El ceilómetro mide la altura de la base de las nubes usando un rayo láser apuntado hacia el cielo.",
    "Las estaciones meteorológicas automáticas combinan sensores para medir temperatura, presión, humedad, viento y lluvia.",
    "El piranómetro se usa para medir la radiación solar incidente.",
    "El evaporímetro mide la cantidad de agua evaporada en una superficie durante un periodo de tiempo.",
]

vectors = model.encode(texts2)
print("vectors shape:",vectors.shape)
# 2️⃣ Conectar con Qdrant

client = QdrantClient(url="http://localhost:6333")  # o tu endpoint cloud
print(client.get_collections())

# 3️⃣ Crear la colección (si no existe)
collection_name = "docs_vectoriales"
collection_name = "docs_vectorialesv2"

if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print(f"✅ Colección '{collection_name}' creada.")
else:
    print(f"⚠️ Colección '{collection_name}' ya existe.")

# 4️⃣ Actualizar configuración del índice HNSW (si deseas tunearlo)
client.update_collection(
    collection_name=collection_name,
    hnsw_config=HnswConfigDiff(
        m=16,
        ef_construct=200,
        # ef_search se configura en query-time, no aquí
    )
)
print("🔧 Índice HNSW configurado correctamente.")

# 5️⃣ Insertar los vectores con payloads (metadatos)
points = [
    PointStruct(id=str(uuid.uuid4()), vector=v, payload={"texto": t})
    for v, t in zip(vectors, texts2)
]

client.upsert(collection_name=collection_name, points=points)
print("📦 Vectores insertados correctamente.")

# 6️⃣ Verificar conteo
count = client.count(collection_name, exact=True)
print(f"📊 Total de documentos: {count.count}")



"""
EN EL FUTURO CON LANGCHAIN
ya no usamos client.upsert() y en su lugar usamos QdrantVectorStore.from_texts()

Antes, cuando trabajabas directamente con Qdrant sin LangChain, la forma normal era:

client.upsert(
    collection_name="docs_100pdfs",
    points=[ ... ]   # vectores + payloads
)


Eso implicaba que tú tenías que:

generar las embeddings manualmente

construir los points (id, vector, payload)

asegurarte que la colección exista

manejar errores, índices, distancias, etc.

Era mucho trabajo.

🚀 Ahora con LangChain → QdrantVectorStore.from_texts()

Cuando usas:

QdrantVectorStore.from_texts(
    texts=chunks_all,
    embedding=embeddings,
    collection_name="docs_100pdfs",
    client=client
)


LangChain hace todo esto por ti:

✔ 1. Crea la colección automáticamente

Si no existe → la crea con el tamaño adecuado de vector.

✔ 2. Genera embeddings

Por ejemplo, con all-MiniLM-L6-v2 genera vectores de 384 dimensiones por cada chunk.

✔ 3. Inserta los puntos en Qdrant

Internamente llama a client.upsert(), pero tú ya no lo ves.

✔ 4. Regresa un VectorStore listo para usar como retriever

Lo puedes usar así:

retriever = vectorstore.as_retriever()

📌 Entonces tu flujo real es:
1. ingest_all_pdfs() → devuelve chunks_all

"""