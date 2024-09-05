import requests
import pandas as pd
import torch
from datasets import load_dataset
from sentence_transformers.util import semantic_search

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "InsertTokenHere"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()
with open('CombinedFilesOutput2.txt') as f:
    texts = f.read().splitlines()
# Perhaps download the model, loading it takes roughly 3 seconds


output = query(texts)
embeddings = pd.DataFrame(output)
embeddings.to_csv("fileNameEmbeddings.csv", index=False)
# These lines can be run first, with the first lines, to create the dataset
# Afterwards, run the code without them

# faqs_embeddings = load_dataset('ProjectL/fileNameEmbeddings')
# This is loading the dataset from hugging face, takes 1-2 seconds longer
# but can probably be done without doing embeddings.to_csv first

faqs_embeddings = load_dataset("csv", data_files="fileNameEmbeddings.csv")
# Loading locally, requires embeddings.to_csv() first


# Corpus ID corresponds with the value 1 below the file name, since it 
# starts from 0 presumably
