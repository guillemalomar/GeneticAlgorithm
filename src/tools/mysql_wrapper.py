import pymysql

from src.model import Individual
from settings import MYSQL_PARAMS


class SQLWrapper:
    def __init__(self):
        self.db = pymysql.connect(
            MYSQL_PARAMS['host'],
            MYSQL_PARAMS['user'],
            MYSQL_PARAMS['pass'],
            MYSQL_PARAMS['db']
        )
        self.cursor = self.db.cursor()
        self.clean_table()

    def clean_table(self):
        self.cursor.execute("TRUNCATE TABLE POPULATION")

    def insert_individual(self, individual):
        sql = "INSERT INTO POPULATION(id, iteration, age, height, speed, arm_length, skin_thickness, strength) VALUES ({}, {}, {}, {}, {}, {}, {})".format(
            individual.iteration,
            individual.age,
            individual.height,
            individual.speed,
            individual.arm_length,
            individual.skin_thickness,
            individual.strength
        )
        self.cursor.execute(sql)

    def delete_individual(self, individual_id):
        sql = "DELETE FROM POPULATION WHERE id = '{}'".format(individual_id)
        self.cursor.execute(sql)

    def obtain_individual(self, individual_id):
        sql = "SELECT * FROM POPULATION WHERE id = '{}'".format(individual_id)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            individual = Individual.create(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7]
            )
            return individual

    def obtain_individuals(self, individual_id):
        sql = "SELECT * FROM POPULATION WHERE id = '{}'".format(individual_id)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        individuals = []
        for row in results:
            individual = Individual.create(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7]
            )
            individuals.append(individual)
        return individuals
