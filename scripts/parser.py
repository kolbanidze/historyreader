from bs4 import BeautifulSoup as BS
from requests import get
from json import dumps as json_encode

# Парсинг содержимого билетов

BASE_URL = "https://xn----7sbb3acajbee5aggvnq.xn--90ais/b"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}

OVERWRITE = False
if not OVERWRITE:
    print("Выполнение этого скрипта перезапишет bilety.json и превью билетов.")
    print("Измените флаг OVERWRITE на True, если хотите продолжить.")
    print("Запускайте скрипт из корня приложения (где лежит start.bat).")
    exit(1)

bilety = []

for i in range(1,26):
    r = get(BASE_URL+f"{i}v1", headers=headers)
    get_html = BS(r.content, 'html.parser')
    res = str(get_html.select_one(".t004 > div > div > div"))
    bilety.append({"Number": i,
                   "Text": res,
                   "Test": [{"Question": "Вопрос 1.",
                             "Answers": ["A", "B", "C", "D"],
                             "CorrectAnswer": "A"},
                            {"Question": "Вопрос 2.",
                             "Answers": ["A", "B", "C", "D"],
                             "CorrectAnswer": "B"},
                            {"Question": "Вопрос 3.",
                             "Answers": ["A", "B", "C", "D"],
                             "CorrectAnswer": "C"},
                            {"Question": "Вопрос 4.",
                             "Answers": ["A", "B", "C", "D"],
                             "CorrectAnswer": "D"},
                            {"Question": "Вопрос 5.",
                             "Answers": ["A", "B", "C", "D"],
                             "CorrectAnswer": "A"}]})

with open("data\\json\\bilety.json", "w") as file:
    file.write(json_encode(bilety))

# Парсинг картинок к билетам
for i in range(1,26):
    r = get(BASE_URL+str(i), headers=headers)
    get_html = BS(r.content, 'html.parser')
    img_path = get_html.find('div', attrs={"class": "t404__img t-bgimg"})["data-original"]
    img = get(img_path, headers=headers).content
    with open(f"data\\images\\{i}.jpeg", "wb") as file:
        file.write(img)