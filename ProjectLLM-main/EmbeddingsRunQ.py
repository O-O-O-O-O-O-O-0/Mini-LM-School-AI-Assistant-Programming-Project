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
# Change URLs depending on the school
urls = ["https://miraloma.sanjuan.edu/",
    "https://miraloma.sanjuan.edu/our-school",
    "https://miraloma.sanjuan.edu/our-school/principals-message",
    "https://miraloma.sanjuan.edu/our-school/administration",
    "https://miraloma.sanjuan.edu/our-school/counseling",
    "https://miraloma.sanjuan.edu/our-school/counseling/course-selection-for-2023-2024",
    "https://miraloma.sanjuan.edu/our-school/counseling/physical-education-pe-options",
    "https://miraloma.sanjuan.edu/our-school/counseling/mental-health-resources",
    "https://miraloma.sanjuan.edu/our-school/counseling/dual-enrollment-take-college-classes-in-high-school",
    "https://miraloma.sanjuan.edu/our-school/counseling/seniors",
    "https://miraloma.sanjuan.edu/our-school/counseling/career-technical-education-cte",
    "https://miraloma.sanjuan.edu/our-school/counseling/college-application-and-recommendation-letter-process",
    "https://miraloma.sanjuan.edu/our-school/counseling/advanced-placement-exams",
    "https://miraloma.sanjuan.edu/our-school/mission-statement",
    "https://miraloma.sanjuan.edu/our-school/calendar",
    "https://miraloma.sanjuan.edu/our-school/bell-schedule",
    "https://miraloma.sanjuan.edu/our-school/handbook",
    "https://miraloma.sanjuan.edu/our-school/alumni",
    "https://miraloma.sanjuan.edu/our-school/assessment-data",
    "https://miraloma.sanjuan.edu/our-school/school-plan-for-student-achievement-spsa",
    "https://miraloma.sanjuan.edu/our-school/school-site-council",
    "https://miraloma.sanjuan.edu/our-school/school-logo-and-uniformity-of-use",
    "https://miraloma.sanjuan.edu/our-school/school-profile",
    "https://miraloma.sanjuan.edu/our-school/food-delivery-policy",
    "https://miraloma.sanjuan.edu/resources",
    "https://miraloma.sanjuan.edu/resources/student-resources",
    "https://miraloma.sanjuan.edu/resources/registrar",
    "https://miraloma.sanjuan.edu/resources/english-language-learners",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-arabic",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-darifarsi",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-pashto",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-russian",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-spanish",
    "https://miraloma.sanjuan.edu/resources/english-language-learners/elac-meetings/elac-meetings-ukrainian",
    "https://miraloma.sanjuan.edu/resources/safety-plans",
    "https://miraloma.sanjuan.edu/resources/attendance",
    "https://miraloma.sanjuan.edu/resources/work-permits",
    "https://miraloma.sanjuan.edu/resources/mira-loma-online-store",
    "https://miraloma.sanjuan.edu/resources/transcripts",
    "https://miraloma.sanjuan.edu/academics",
    "https://miraloma.sanjuan.edu/academics/programs",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate/ibpo-registration-information",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate/ib-exam-tips",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate/ibdp",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate/ibmyp",
    "https://miraloma.sanjuan.edu/academics/programs/international-baccalaureate/ibcp",
    "https://miraloma.sanjuan.edu/academics/programs/international-studies-program",
    "https://miraloma.sanjuan.edu/academics/programs/special-education",
    "https://miraloma.sanjuan.edu/academics/library",
    "https://miraloma.sanjuan.edu/academics/college-career",
    "https://miraloma.sanjuan.edu/academics/english",
    "https://miraloma.sanjuan.edu/academics/historysocial-science",
    "https://miraloma.sanjuan.edu/academics/math",
    "https://miraloma.sanjuan.edu/academics/physical-education",
    "https://miraloma.sanjuan.edu/academics/science",
    "https://miraloma.sanjuan.edu/academics/visual-and-performing-arts",
    "https://miraloma.sanjuan.edu/academics/world-languages",
    "https://miraloma.sanjuan.edu/activities",
    "https://miraloma.sanjuan.edu/athletics",
    "https://miraloma.sanjuan.edu/athletics/registration",
    "https://miraloma.sanjuan.edu/athletics/list-of-sports-by-season",
    "https://miraloma.sanjuan.edu/connect",
    "https://miraloma.sanjuan.edu/connect/staff-directory",
    "https://miraloma.sanjuan.edu/connect/get-involved",
    "https://miraloma.sanjuan.edu/connect/social-media",
    "https://miraloma.sanjuan.edu/connect/facilities-use",
    "https://miraloma.sanjuan.edu/news",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/mira-loma-news/post/ibmyp-application",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/mira-loma-news/post/campus-tours",
    "https://miraloma.sanjuan.edu/fs/pages/12931",
    "https://miraloma.sanjuan.edu/fs/pages/12898",
    "https://miraloma.sanjuan.edu/fs/pages/12930",
    "https://miraloma.sanjuan.edu/site-map",
    "https://miraloma.sanjuan.edu/fs/pages/27053",
    "https://miraloma.sanjuan.edu/fs/pages/6078",
    "https://miraloma.sanjuan.edu/connect/staff-directory?const_page=1&",
    "https://miraloma.sanjuan.edu/connect/staff-directory?const_page=2&",
    "https://miraloma.sanjuan.edu/connect/staff-directory?const_page=3&",
    "https://miraloma.sanjuan.edu/fs/pages/6171",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/a-note-from-superintendent-bassanelli-a-message-of-reflection-and-gratitude",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-nov-14-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/mira-loma-high-school-celebrates-da-de-los-muertos",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-oct-24-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/a-note-from-superintendent-bassanelli-san-juan-unifieds-career-opportunities-are-waiting-for-you",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/provide-input-on-proposed-instructional-materials",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-oct-11-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/mira-loma-news/post/winter-sports",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-sept-26-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/san-juan-unified-community-celebrates-bright-futures-at-college-night-event",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/san-juan-unifieds-school-bus-academy-drives-its-students-to-success",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-sept-12-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/a-note-from-superintendent-bassanelli-we-cant-wait-to-see-your-student-on-aug-10-1694539837680",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/mira-loma-news/post/senior-portraits-2023",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/share-your-voice-by-joining-a-district-committee",
    "https://miraloma.sanjuan.edu/news/news-detail/~board/district-news/post/board-briefs-aug-22-2023",
    "https://miraloma.sanjuan.edu/fs/pages/477",
    "https://miraloma.sanjuan.edu/fs/pages/559"]

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()

# Perhaps download the model, loading it takes roughly 3 seconds

def run_embeddings(faqs_embeddings, inputQuestion):
    # Loading locally, requires precreated embeddings.to_csv() to function
    dataset_embeddings = torch.from_numpy(faqs_embeddings["train"].to_pandas().to_numpy()).to(torch.float)
    question = [inputQuestion]
    output = query(question)
    query_embeddings = torch.FloatTensor(output)
    # Change top_k to change the number of queries. Currently it's 5*5, decrease for faster speed
    hits = semantic_search(query_embeddings, dataset_embeddings, top_k=5)
    # print([texts[hits[0][i]['corpus_id']] for i in range(len(hits[0]))])
    return hits

# Basically, this just runs the program, doing 2 queries within the vector embeddings files.
# The first query finds the correct files, while the second query is within the files.
def run_everything(inputQ):
    faqs_embeddings = load_dataset("csv", data_files="fileNameEmbeddings.csv")
    hits = run_embeddings(faqs_embeddings, inputQ)
    total_hits = []
    new_texts = []
    links = [""] * 5
    for num in range(5):
        tempTxtName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-" + str(hits[0][num]['corpus_id'] + 1)
        with open(tempTxtName) as f:
            texts = f.read().splitlines()
        new_texts.append(texts)
        # embeddings = pd.DataFrame(output) 
        tempFileName = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFileEmbeddings/fileEmbeddings" + str(hits[0][num]['corpus_id'] + 1) + ".csv"
        # embeddings.to_csv(tempFileName, index=False)
        faqs_embeddings = load_dataset("csv", data_files=tempFileName)
        temp_hits = run_embeddings(faqs_embeddings, inputQ)
        total_hits += [temp_hits]
        tempStr = urls[int(hits[0][num]['corpus_id'])]
        tempStr2 = ""
        for val in tempStr:
            tempStr2 += val
        links[num] += tempStr2
    max_hits = []
    for j in range(5):
        # Setting fileID as j, instead of just putting j in for distinction 
        # between the uses, even though the values are the same
        fileID = j
        max_hits += [[[item['score'], item['corpus_id'], fileID]for item in total_hits[j][0]]]
    # Maybe add it all to same list, and then sort
    sorted_max = sorted(max_hits, key=lambda x: list(x[0])[0], reverse=True)
    sorted_max_hits = [item[0] for item in sorted_max]
    for_printing = [new_texts[item[2]][item[1]] for item in sorted_max_hits]
    for num in range(len(for_printing)):
        for_printing[num] = for_printing[num].replace(u'\xa0', u' ')
    scores = [[item[0]]for item in sorted_max_hits]
    return for_printing, scores, links
