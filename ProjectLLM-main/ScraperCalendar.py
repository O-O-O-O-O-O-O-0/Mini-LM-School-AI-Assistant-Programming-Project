import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# This is specifically to scrape the calendar page of Miraloma, which is a pain
# as it's very different from the rest of the pages
url = 'https://miraloma.sanjuan.edu/our-school/calendar'

# Send GET request
response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with these specific classes
    specific_class_elements = soup.find_all(class_='fsCalendarInfo')
    specific_class_elements2 = soup.find_all(class_='fsTimeRange')
    timeElements = []
    textWithTime = []
    textWithOutTime = []
    for element in specific_class_elements:
        time_element = element.find('time')
        if time_element:
            # Convert to PST
            datetime_value = time_element['datetime']
            datetime_object = datetime.fromisoformat(datetime_value.replace("T", " ").split(".")[0])
            pst_timezone = pytz.timezone('US/Pacific')  # 'US/Pacific' is the timezone identifier for PST
            datetime_object_pst = datetime_object.astimezone(pst_timezone)
            formatted_result = datetime_object_pst.strftime('%Y-%m-%d %I:%M:%S %p')
            timeElements.append(f'{formatted_result}\n')
            textWithTime.append(element)
        else:
            textWithOutTime.append(element)
    adder = 0
    for num in range(len(textWithTime)):
        textWithTime.insert(num + adder + 1, timeElements[num])
        adder+=1
    for num in range(len(textWithOutTime)):
        if (element.txt != "Subscribe to Alerts"):
            textWithTime.append(textWithOutTime[num])
    
    # print(timeElements)
    # Change this to wherever you want the calendar info to go. The original calendar page
    # is the 15th URL, which is why I use output-15
    finalOutput = "/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-15"
    # finalOutput = "ScraperCalendarTest.txt"
    # Create or open a file to write the data
    prev_element = textWithTime[0]
    with open(finalOutput, 'w', encoding='utf-8') as file:
        # Loop to write information to the file
        for element in textWithTime:
            if type(element) != str:
                title_element = element.find('a', class_='fsCalendarEventTitle fsCalendarEventLink')
                if title_element:
                    # Extract and print the text from the title element
                    file.write(title_element.text.strip() + ': ')
                    if prev_element != textWithTime[0] and '202' not in element and '202' not in prev_element:
                        file.write('\n')
            else:
                file.write(element)
            prev_element = element
        for element in textWithOutTime:
            if (element.txt != "Subscribe to Alerts"):
                title_element = element.find('a', class_='ae-compliance-indent ae-reader-visible')
                if title_element:
                    file.write(title_element.text.strip() + '\n')

    print('Data has been successfully written to output-15')

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
