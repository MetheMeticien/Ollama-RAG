import ollama, sys, chromadb, time
from utilities import getconfig


embedmodel = getconfig()["embedmodel"]
mainmodel = getconfig()["mainmodel"]
chroma = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma.get_or_create_collection("buildragwithpython")

query = " ".join(sys.argv[1:])
queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']

start = time.time()

relevantdocs = collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
docs = "\n\n".join(relevantdocs)

print(docs)

end = time.time()
print(end - start)


modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"


stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)


for chunk in stream:
  if chunk["response"]:
    print(chunk['response'], end='', flush=True)

end = time.time()
print(end - start)
