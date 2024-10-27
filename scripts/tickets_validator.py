# Валидатор билетов

from json import loads

with open("..\\data\\json\\bilety.json", "r", encoding="utf-8") as file:
    bilety = loads(file.read())

tickets_numbers = []

for i in bilety:
    tickets_numbers.append(i["Number"])
    if len(i["Text"]) < 1:
        print('='*32)
        print(f"Ticket {i['Number']} is empty.")
        print('='*32)
    test = i["Test"]
    for j in test:
        if len(j["Question"]) < 1:
            print('='*32)
            print(f"Question ticket {i['Number']} is empty.")
            print('='*32)
        answers = j["Answers"]
        correct_answer = j["CorrectAnswer"]
        if correct_answer not in answers:
            print('='*32)
            print(f"Question ticket {i['Number']} is MALFORMED.")
            print("Question:", j["Question"])
            print('='*32)

if tickets_numbers != [i for i in range(1,26)]:
    print("Номера билетов не соответствуют 1..25")