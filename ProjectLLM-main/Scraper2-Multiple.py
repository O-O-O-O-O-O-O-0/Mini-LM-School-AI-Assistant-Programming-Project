import requests
from bs4 import BeautifulSoup
import json
import re

# Function to check if the paragraph contains an email address and keeps only one copy
# This is really a relic, but it's kept just in case for the future
def contains_email(text, seen_emails):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    for match in matches:
        if match not in seen_emails:
            seen_emails.add(match)
        else:
            text = text.replace(match, '')
    return text, seen_emails

seen_emails = set()
unique_data = []

# List of URLs to scrape. Change for other schools
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

count = 1
for url in urls:
    fileName = '/Users/sriharithirumaligai/Downloads/project1-main/ListOfFiles/output-'
    fileName += str(count)
    # send a GET request to the URL
    response = requests.get(url)
    print("Past output-" + str(count))

    # if the request was not successful, print an error message and move onto next
    if response.status_code != 200:
        print(f'Error: Got status code {response.status_code} for URL: {url}')
        count += 1
        fileName += str(count)
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the paragraph elements in the HTML
    paragraphs = soup.find_all('p')
    notFound = True
    # Just getting rid of repetitive, unimportant stuff in the HTML that shows on every page unnecessarily
    repetitiveStuff = ["Non-Discrimination Statement:The San Juan Unified School District Board of Education is committed to equal opportunity for all individuals in district programs and activities. District programs, activities and services shall be free from unlawful discrimination, harassment (including sexual harassment), intimidation, and/or bullying based on actual or perceived characteristics of race or ethnicity, color, ancestry, nationality, national origin, immigration status, ethnic group identification, age, religion, marital or parental status, pregnancy, physical or mental disability, sex, sexual orientation, gender, gender identity, gender expression, genetic information, affiliation with the Boy Scouts of America, or on the basis of a person's association with a person or group with one or more of these actual or perceived characteristics. If you believe you have experienced unlawful discrimination, please contact: Equity Compliance Officer, Fhanysha C. Gaddis, (916) 971-7110, LegalServices@sanjuan.edu; Title IX Coordinator, Katie Fabel, (916) 971-7110, TitleIX@sanjuan.edu; Section 504 Coordinator, Dominic Covello, (916) 971-7220; ADA/Title II Coordinator, Michelle Fischer, (916) 971-7036", "TitleIX@sanjuan.edu","LegalServices@sanjuan.edu", "Charles Peck Elementary School is currently in a precautionary shelter-in-place due to an unknown person on campus. Law enforcement has been notified. Please do not go to the campus at this time. An update will be provided as soon as it is available."]
    for paragraph in paragraphs:
        for string in repetitiveStuff:
            if string in paragraph.get_text(strip=True):
                notFound = False
                break
        if notFound:
            text, seen_emails = contains_email(paragraph.get_text(strip=True), seen_emails)
            unique_data.append(text)
        notFound = True

    # Save data to file, encoded with utf-8
    with open(fileName, 'w', encoding='utf-8') as file:
        # Encode non-ASCII characters in a way compatible with utf-8
        unique_data_encoded = "\n".join(unique_data).encode('utf-8', 'ignore').decode('utf-8')
        seen_emails_encoded = '\n'.join(seen_emails).encode('utf-8', 'ignore').decode('utf-8')

        file.write(f"{unique_data_encoded}\n\n\n{seen_emails_encoded}\n")

    unique_data.clear()
    seen_emails.clear()

    count += 1
