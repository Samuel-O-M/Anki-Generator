import requests
from bs4 import BeautifulSoup

def categorize(word, language="Russian"):      
        
    url = 'https://en.wiktionary.org/wiki/' + word
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    soup = str(soup)

    sections = soup.split("catlinks")[0].split("mw-heading2")

    targetSection = None

    for i in range(1, len(sections)):
        if f'id="{language}"' in sections[i]:
            targetSection = sections[i]
            break

    if targetSection == None:
        return "word not found"

    tags = ["Noun", "Verb", "Adjective", "Adverb", "Pronoun", "Numeral"]


    # Find the first (most common) use of the word
    
    tag_positions = {t: targetSection.find(t) for t in tags if t in targetSection}
    
    if not tag_positions:
        return "other"
    
    min_position_tag = min(tag_positions, key=tag_positions.get)
    
    return min_position_tag.lower()


    # Find all uses of the word

    # matchingTags = [t for t in tags if t in targetSection]
    
    # if len(matchingTags) == 1:
    #     return matchingTags[0].lower()
    # elif len(matchingTags) > 1:
    #     return "error"
    # else:
    #     return "other"

if __name__ == "__main__":

    print(categorize("красивый"))
    print(categorize("красиво"))
    print(categorize("красивость"))
    print(categorize("красив"))
    print(categorize("они"))