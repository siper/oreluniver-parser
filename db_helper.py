import psycopg2
import os

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


class PostgreSQLHelper:
    def __init__(self):
        pass

    def __enter__(self):
        self.connection = psycopg2.connect(user=DB_USER,
                                           password=DB_PASSWORD,
                                           host=DB_HOST,
                                           port=DB_PORT,
                                           database=DB_NAME)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.close()
        except Exception:
            pass


class BuildingsDao(PostgreSQLHelper):
    def _delete_buildings_table(self):
        query = '''DROP TABLE IF EXISTS buildings'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_buildings_table(self):
        query = '''CREATE TABLE IF NOT EXISTS buildings
                          (id INT PRIMARY KEY NOT NULL,
                          title TEXT,
                          address TEXT,
                          latitude float8,
                          longitude float8,
                          img TEXT);'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_buildings(self, buildings):
        self._delete_buildings_table()
        self._create_buildings_table()

        cursor = self.connection.cursor()
        for building in buildings:
            query = '''INSERT INTO buildings (id, title, address, latitude, longitude, img) 
                       VALUES ({}, '{}', '{}', {}, {}, '{}');'''.format(building["id"],
                                                                        building["title"],
                                                                        building["address"],
                                                                        building["latitude"],
                                                                        building["longitude"],
                                                                        building["img"])
            cursor.execute(query)
        self.connection.commit()


class ClassroomsDao(PostgreSQLHelper):
    def _delete_classrooms_table(self):
        query = '''DROP TABLE IF EXISTS classrooms'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_classrooms_table(self):
        query = '''CREATE TABLE IF NOT EXISTS classrooms
                          (id INT PRIMARY KEY NOT NULL,
                          title TEXT NOT NULL,
                          building_id INT NOT NULL);'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_classrooms(self, classrooms):
        self._delete_classrooms_table()
        self._create_classrooms_table()

        cursor = self.connection.cursor()
        for classroom in classrooms:
            query = '''INSERT INTO classrooms (id, title, building_id) 
                               VALUES ({}, '{}', {});'''.format(classroom["id"],
                                                                classroom["title"],
                                                                classroom["building_id"])
            cursor.execute(query)
        self.connection.commit()


class GroupsDao(PostgreSQLHelper):
    def _delete_groups_table(self):
        query = '''DROP TABLE IF EXISTS groups'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_groups_table(self):
        query = '''CREATE TABLE IF NOT EXISTS groups
                          (id INT PRIMARY KEY NOT NULL,
                          title TEXT NOT NULL,
                          course INT NOT NULL,
                          code TEXT NOT NULL,
                          education_level TEXT NOT NULL,
                          institute_id INT NOT NULL
                          );'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_groups(self, groups):
        self._delete_groups_table()
        self._create_groups_table()

        cursor = self.connection.cursor()
        for group in groups:
            query = '''INSERT INTO groups (id, title, course, code, education_level, institute_id) 
                               VALUES ({}, '{}', '{}', '{}', '{}', {});'''.format(group["id"],
                                                                                  group["title"],
                                                                                  group["course"],
                                                                                  group["code"],
                                                                                  group["education_level"],
                                                                                  group["institute_id"])
            cursor.execute(query)
        self.connection.commit()


class TeachersDao(PostgreSQLHelper):
    def _delete_teachers_table(self):
        query = '''DROP TABLE IF EXISTS teachers'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_teachers_table(self):
        query = '''CREATE TABLE IF NOT EXISTS teachers
                          (id INT PRIMARY KEY NOT NULL,
                          name TEXT NOT NULL,
                          surname TEXT NOT NULL,
                          patronymic TEXT NOT NULL,
                          photo TEXT,
                          chair_id INT NOT NULL
                          );'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_teachers(self, teachers):
        self._delete_teachers_table()
        self._create_teachers_table()

        cursor = self.connection.cursor()
        for teacher in teachers:
            query = '''INSERT INTO teachers (id, name, surname, patronymic, photo, chair_id) 
                               VALUES ({}, '{}', '{}', '{}', '{}', {}) 
                               ON CONFLICT (id) DO NOTHING;'''.format(teacher["id"],
                                                                      teacher["name"],
                                                                      teacher["surname"],
                                                                      teacher["patronymic"],
                                                                      teacher["photo"],
                                                                      teacher["chair_id"])
            cursor.execute(query)
        self.connection.commit()


class InstitutesDao(PostgreSQLHelper):
    def _delete_institutes_table(self):
        query = '''DROP TABLE IF EXISTS institutes'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_institutes_table(self):
        query = '''CREATE TABLE IF NOT EXISTS institutes
                          (id INT PRIMARY KEY NOT NULL,
                          title TEXT NOT NULL,
                          short_title TEXT NOT NULL);'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_institutes(self, institutes):
        self._delete_institutes_table()
        self._create_institutes_table()

        cursor = self.connection.cursor()
        for institute in institutes:
            query = '''INSERT INTO institutes (id, title, short_title) 
                               VALUES ({}, '{}', '{}') 
                               ON CONFLICT (id) DO NOTHING;'''.format(institute["id"],
                                                                      institute["title"],
                                                                      institute["short_title"])
            cursor.execute(query)
        self.connection.commit()


class ChairsDao(PostgreSQLHelper):
    def _delete_chairs_table(self):
        query = '''DROP TABLE IF EXISTS chairs'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def _create_chairs_table(self):
        query = '''CREATE TABLE IF NOT EXISTS chairs
                          (id INT PRIMARY KEY NOT NULL,
                          title TEXT NOT NULL,
                          short_title TEXT NOT NULL,
                          institute_id INT NOT NULL);'''
        cursor = self.connection.cursor()
        cursor.execute(query)

    def put_chairs(self, chairs):
        self._delete_chairs_table()
        self._create_chairs_table()

        cursor = self.connection.cursor()
        for chair in chairs:
            query = '''INSERT INTO chairs (id, title, short_title, institute_id) 
                               VALUES ({}, '{}', '{}', {}) 
                               ON CONFLICT (id) DO NOTHING;'''.format(chair["id"],
                                                                      chair["title"],
                                                                      chair["title"],
                                                                      chair["institute_id"])
            cursor.execute(query)
        self.connection.commit()
