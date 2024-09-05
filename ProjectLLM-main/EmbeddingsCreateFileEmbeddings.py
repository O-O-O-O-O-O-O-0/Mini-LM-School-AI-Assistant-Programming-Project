import requests
import pandas as pd
import torch
from datasets import load_dataset
from sentence_transformers.util import semantic_search

model_id = "sentence-transformers/all-MiniLM-L6-v2"
# Put in your own hugging face token
hf_token = "InsertTokenHere"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()
with open('CombinedFilesOutput2.txt') as f:
    texts = f.read().splitlines()
# Perhaps download the model, loading it takes roughly 3 seconds

def run_embeddings(faqs_embeddings, inputQuestion):
    # Loading locally, requires precreated embeddings.to_csv() to function
    dataset_embeddings = torch.from_numpy(faqs_embeddings["train"].to_pandas().to_numpy()).to(torch.float)
    question = [inputQuestion]
    output = query(question)
    query_embeddings = torch.FloatTensor(output)
    hits = semantic_search(query_embeddings, dataset_embeddings, top_k=5)
    # print([texts[hits[0][i]['corpus_id']] for i in range(len(hits[0]))])
    print(hits[0][1]['corpus_id'])
    return hits

# Creating the individual file embeddings
for num in range(99):
    tempTxtName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-" + str(num + 1)
    with open(tempTxtName) as f:
        texts = f.read().splitlines()
    output = query(texts)
    embeddings = pd.DataFrame(output) 
    tempFileName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFileEmbeddings/fileEmbeddings" + str(num+1) + ".csv"
    embeddings.to_csv(tempFileName, index=False)
    print("Finished output-", num+1, sep = "")

# The file IDs should be in order, so add another file_id component and then
# have it be based numerically, smallest file as 0 up to n based on top_k=n
