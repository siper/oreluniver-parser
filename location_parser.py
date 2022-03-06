import requests
import json
import db_helper
from collections import OrderedDict


class Iterator:
    def __iter__(self):
        self.a = 0
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


def get_buildings():
    r = requests.get("http://oreluniver.ru/assets/js/buildings.json")
    j = json.loads(r.text.lstrip('\ufeff'))
    print(j["corpusData"])
    return j["corpusData"]


def get_rooms(building_id):
    r = requests.get("http://oreluniver.ru/schedule/{}/auditlist".format(building_id))
    j = json.loads(r.text)
    result = []
    for r in j:
        room = r["NumberRoom"].strip()
        if room != "":
            result.append(room)
    return result


def parse_all():
    b_it = iter(Iterator())
    l_it = iter(Iterator())

    buildings = []
    classrooms = []

    for b in get_buildings():
        building_id = next(b_it)
        building = OrderedDict(id=building_id,
                               title=b["title"],
                               address=b["address"],
                               latitude=b["coord"][0],
                               longitude=b["coord"][1],
                               img=b["img"])
        buildings.append(building)

        print("Added building with id {}".format(building_id))

        for r in get_rooms(building_id):
            classroom = OrderedDict(id=next(l_it), title=r, building_id=building_id)
            classrooms.append(classroom)

            print("Added classroom with id {}".format(id))

    with db_helper.ClassroomsDao() as dao:
        dao.put_classrooms(classrooms)

    with db_helper.BuildingsDao() as dao:
        dao.put_buildings(buildings)

    print("All done")


if __name__ == "__main__":
    parse_all()
