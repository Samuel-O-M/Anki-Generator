import csv

def create_flashcards(data):

    with open('data/cards.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        field = ["Top", "Russian", "Audio", "English", "Spanish", "Example Russian 1", "Example Russian 2", "Example Russian 3", "Audio 1", "Audio 2", "Audio 3", "Example English 1", "Example English 2", "Example English 3", "Example Spanish 1", "Example Spanish 2", "Example Spanish 3", "Tag"]
        writer.writerow(field)
        
        for array in data:
                writer.writerow(array)
