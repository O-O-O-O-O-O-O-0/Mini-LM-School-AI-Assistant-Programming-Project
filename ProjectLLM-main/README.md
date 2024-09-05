---
title: ProjectLLM-main
app_file: GradioTests.py
sdk: gradio
sdk_version: 4.9.1
---
### Notes:

Use your own hugging face token, in place of 'InsertTokenHere'

Change the file locations as necessary so that it works on your device
  
Here is the order of files to run:
- Scraper2-Multiple.py (This will create the files for the web links)
- ScraperCalendar.py (This scrapes the calendar link, and adds it to the list)
- CreateFullFile.py (Adds all of the content to a singular file, in order to create the embeddings)
- EmbeddingsCombinedFilesOutput2.py(This creates embeddings for the combined file)
- EmbeddingsCreateFileEmbeddings.py(Creates the individual embeddings)
- EmbeddingsCombinedFilesMultipleQueries.py(Put in your question as inputQ)
- GradioTests.py(To use the Gradio link)

Future Plans:
1. Improve Scraping Algorithms
2. Improve Cosine Similarity Search (if possible)
3. Create Student View
4. Work With More Schools
