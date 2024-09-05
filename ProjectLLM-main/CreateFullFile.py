# Specify the directory path to where your files are stored
file_name = '/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-'
# Specify the directory path to where your combined output will be stored
combined_file_path = '/Users/sriharithirumaligai/Downloads/project1-main/CombinedFilesOutput2.txt'

# Open the combined file in write mode to clear it
with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
    pass

# Iterate through each of the 100 web pages in Mira Loma High School's website 
# (change the 100 for other schools)
for file_number in range(1, 100):
    output_string = ""
    
    # Construct file path
    file_path = f'{file_name}{file_number}'  

    # Open and read file's content, and put it all into output_string, replacing newlines
    with open(file_path, 'r', encoding='utf-8') as current_file:
        file_content = current_file.read()
    for paragraph in file_content:
        output_string += paragraph
    output_string = output_string.replace("\n", " ")
    # Append the content to the combined file on a new line
    with open(combined_file_path, 'a', encoding='utf-8') as combined_file:
        combined_file.write(output_string + "\n")
