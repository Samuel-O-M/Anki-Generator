import requests
from bs4 import BeautifulSoup
import re 

def rank(n):

    if not isinstance(n, int):
        n = int(n)

    if 1 <= n <= 1000:
        interval = "1-1000"
    elif 1001 <= n <= 2000:
        interval = "1001-2000"
    elif 2001 <= n <= 3000:
        interval = "2001-3000"
    elif 3001 <= n <= 4000:
        interval = "3001-4000"
    elif 4001 <= n <= 5000:
        interval = "4001-5000"
    else:
        interval = "error"
    
    next_n = n + 1
    n = str(n)
    next_n = str(next_n)

    url = 'https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/' + interval
    response = requests.get(url)
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    soup = str(soup)

    table = soup.split("</table>")[0]


    if interval.find(n) > 0:
        part = table.split(f"<td>{n}")[1]

    else:
        part = table.split(f"<td>{n}")[1].split(f"<td>{next_n}")[0]

    word = re.search(r'title="(.*?)"', part)
    if word:
        word = word.group(1)
    else:
        word = "error"

    count = part.split("href")[0].count("<td>")

    categoryList = ["noun", "verb", "adjective", "adverb", "numeral", "other"]
    category = categoryList[count - 1]

    return word, category
