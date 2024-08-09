import csv

def create_flashcards(header, content):

    with open('data/cards.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(header)
        
        for row in content:
                writer.writerow(row)
