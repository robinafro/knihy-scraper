import json

data = json.load(open('books.json', 'r', encoding='utf-8'))

formatted_data = {}

for category, info in data.items():
    books = info["books"]
    minimum_count = info["minium_count"]

    formatted_data[category] = {"books": []}

    for book in books:
        formatted_data[category]["books"].append({"name": book})

# Print the formatted data
print(formatted_data)

json.dump(formatted_data, open('books.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)