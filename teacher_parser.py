import requests
import json
import db_helper
from collections import OrderedDict
from bs4 import BeautifulSoup


def get_institutes():
    teachers = requests.get("http://oreluniver.ru/schedule/divisionlistforpreps")
    groups = requests.get("http://oreluniver.ru/schedule/divisionlistforstuds")
    result = []
    result.extend(parse_institutes(teachers.text))
    for i in parse_institutes(groups.text):
        if i not in result:
            result.append(i)
    return result


def parse_institutes(text):
    json_reader = json.loads(text)
    result = []
    for e in json_reader:
        res = OrderedDict(id=int(e["idDivision"]),
                          title=e["titleDivision"].strip(),
                          short_title=e["shortTitle"].strip())
        result.append(res)
    return result


def get_chairs(institute_id):
    r = requests.get("http://oreluniver.ru/schedule/{}/kaflist".format(institute_id))
    json_reader = json.loads(r.text)
    result = []
    for e in json_reader:
        res = OrderedDict(id=int(e["idDivision"]),
                          title=e["titleDivision"].strip(),
                          short_title=e["shortTitle"].strip(),
                          institute_id=int(institute_id))
        result.append(res)
    return result


def get_teachers(chair_id):
    r = requests.get("http://oreluniver.ru/schedule/{}/preplist".format(chair_id))
    json_reader = json.loads(r.text)
    result = []
    for e in json_reader:
        res = OrderedDict(id=int(e["employee_id"]),
                          photo=get_photo(e["employee_id"]).strip(),
                          name=e["Name"].strip(),
                          surname=e["Family"].strip(),
                          patronymic=e["SecondName"].strip(),
                          chair_id=int(chair_id))
        result.append(res)
    return result


def get_photo(teacher_id):
    r = requests.get("http://oreluniver.ru/employee/{}".format(teacher_id))
    soup = BeautifulSoup(r.text, 'html.parser')
    fphoto = soup.find(class_="img-circle")
    if fphoto is None:
        return ""
    photo = fphoto["src"]
    if len(photo) == 0:
        return ""
    if photo.startswith("http"):
        return photo
    else:
        return "http://oreluniver.ru" + photo


def cache_into_db():
    requests.post("https://nosnch.in/c15c01bfe3", data={"m": "Started parse teachers"})
    teachers = []
    chairs = []
    institutes = get_institutes()
    for i in institutes:
        print("Institute")
        print(i["title"])

        c = get_chairs(i["id"])
        chairs.extend(c)

        for chair in c:
            print("Chair")
            print(chair["title"])
            for t in get_teachers(chair["id"]):
                print("Teacher with id {} added".format(t["id"]))
                teachers.append(t)

    with db_helper.TeachersDao() as dao:
        dao.put_teachers(teachers)

    with db_helper.ChairsDao() as dao:
        dao.put_chairs(chairs)

    with db_helper.InstitutesDao() as dao:
        dao.put_institutes(institutes)

    requests.post("https://nosnch.in/c15c01bfe3", data={"m": "Endded parse teachers"})


if __name__ == "__main__":
    cache_into_db()
