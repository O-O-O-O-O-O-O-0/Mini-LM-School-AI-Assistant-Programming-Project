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

output = query(texts)
# embeddings = pd.DataFrame(output)
# embeddings.to_csv("fileNameEmbeddings.csv", index=False)
# These lines can be run first, with the first lines, to create the dataset
# Afterwards, run the code without them

# faqs_embeddings = load_dataset('ProjectL/fileNameEmbeddings')
# This is loading the dataset from hugging face, takes 1-2 seconds longer
# but can be done without doing embeddings.to_csv first if uploaded

faqs_embeddings = load_dataset("csv", data_files="fileNameEmbeddings.csv")

# Condensed searching the embeddings for an output. Change function instead
# Returning hits, which is the top_k=5 closest results
inputQ = "What is the IB program?"
hits = run_embeddings(faqs_embeddings, inputQ)

# hits[0][1]['corpus_id'] gives the ID of the file, starting from 0. 
# The file's name is "output-" + hits[0][1]['corpus_id'] + 1


total_hits = []
new_texts = []
for num in range(5):
    tempTxtName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-" + str(hits[0][num]['corpus_id'] + 1)
    with open(tempTxtName) as f:
        texts = f.read().splitlines()
    new_texts.append(texts)
    output = query(texts)
    # embeddings = pd.DataFrame(output) 
    tempFileName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFileEmbeddings/fileEmbeddings" + str(hits[0][num]['corpus_id'] + 1) + ".csv"
    # embeddings.to_csv(tempFileName, index=False)
    faqs_embeddings = load_dataset("csv", data_files=tempFileName)
    temp_hits = run_embeddings(faqs_embeddings, inputQ)
    total_hits += [temp_hits]

# The file IDs should be in order, so add another file_id component and then
# have it be based numerically, smallest file as 0 up to n based on top_k=n

max_hits = []
# Finding the score values, putting them in an array
for j in range(5):
    # Setting fileID as j, instead of just putting j in for distinction 
    # between the uses, even though the values are the same
    fileID = j
    max_hits += [[[item['score'], item['corpus_id'], fileID]for item in total_hits[j][0]]]
sorted_max_hits = sorted(max_hits, key=lambda x: list(x[0])[0], reverse=True)

# print(sorted_max_hits)
# print(new_texts)
for_printing =[new_texts[item[2]][item[1]] for item in sorted_max_hits[0]]
for i in range(len(for_printing)):
    print(for_printing[i])
