import requests
import json
from bs4 import BeautifulSoup


# extract text from url
def extract_content_from_url(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # extract paragraphs
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content[:1000]  # output first 1000 characters
    except Exception as e:
        return f"Error fetching content from {url}: {e}"


# Input Search Query
search_query = input("Enter a search query: ")

url = "https://google.serper.dev/search"

payload = json.dumps({
    "q": search_query
})

# Get a free google search api key from this site https://serper.dev/
headers = {
    # 'X-API-KEY': 'copy paste your api key here and uncomment',
    'Content-Type': 'application/json'
}


response = requests.post(url, headers=headers, data=payload)


result = json.loads(response.text)

# Display relevant information from the response
if 'organic' in result:
    print(f"\nSearch Results for: {search_query}\n")

    summaries = []

    for index, item in enumerate(result['organic'], start=1):
        print(f"{index}. {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Snippet: {item['snippet']}\n")

        # Fetch content from each link and generate a summary
        page_content = extract_content_from_url(item['link'])
        summaries.append(page_content)

    # Combine summaries into a single paragraph
    summary_paragraph = ' '.join(summaries[:3])
    print("\nGenerated Summary:\n")
    print(summary_paragraph)
else:
    print("No results found")
