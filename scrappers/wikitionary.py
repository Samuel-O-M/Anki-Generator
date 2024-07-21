import requests
from bs4 import BeautifulSoup

def categorize(word):      
        
    url = 'https://en.wiktionary.org/wiki/' + word
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    soup = str(soup)

    sections = soup.split("catlinks")[0].split("mw-heading2")

    russianSection = None

    for i in range(1, len(sections)):
        if 'id="Russian"' in sections[i]:
            russianSection = sections[i]
            break

    tags = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", "Numeral"]

    matchingTags = [t for t in tags if t in russianSection]
    
    if len(matchingTags) == 1:
        return matchingTags[0].lower()
    elif len(matchingTags) > 1:
        return "error"
    else:
        return "other"

if __name__ == "__main__":

    print(categorize("красивый"))
    print(categorize("красиво"))
    print(categorize("красивость"))
    print(categorize("красив"))
    print(categorize("они"))