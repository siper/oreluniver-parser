import requests
import json
import db_helper
from collections import OrderedDict


def get_institutes():
    r = requests.get("http://oreluniver.ru/schedule/divisionlistforstuds")
    json_reader = json.loads(r.text)
    result = []
    for e in json_reader:
        res = OrderedDict(id=int(e["idDivision"]),
                          title=e["titleDivision"].strip(),
                          short_title=e["shortTitle"].strip())
        result.append(res)
    return result


def get_courses(institute_id):
    r = requests.get("http://oreluniver.ru/schedule/{}/kurslist".format(institute_id))
    json_reader = json.loads(r.text)
    result = []
    for e in json_reader:
        # res = OrderedDict(id=int(e["idDivision"]), title=e["titleDivision"], short_title=e["shortTitle"])
        result.append(int(e["kurs"]))
    return result


def get_groups(institute_id, course):
    r = requests.get("http://oreluniver.ru/schedule/{}/{}/grouplist".format(institute_id, course))
    json_reader = json.loads(r.text)
    result = []
    for e in json_reader:
        res = OrderedDict(id=int(e["idgruop"]),
                          title=e["title"].strip(),
                          course=int(course),
                          code=e["Codedirection"].strip(),
                          education_level=e["levelEducation"].strip(),
                          institute_id=int(institute_id))
        result.append(res)
    return result


def parse_all():
    groups = []
    for i in get_institutes():
        for c in get_courses(i["id"]):
            for g in get_groups(i["id"], c):
                print("Group with id {} added".format(g["id"]))
                groups.append(g)

    with db_helper.GroupsDao() as dao:
        dao.put_groups(groups)

    print("All done")


if __name__ == "__main__":
    parse_all()
