from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_teams(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t.* , sum(s.salary) somma_salari
        from salaries s , teams t 
        where s.teamID = t.ID and s.`year` = %s and t.`year` = s.`year`
        group by t.ID """
        cursor.execute(query, (anno,))
        result = []
        for row in cursor:
            result.append(Team(**row))
        cursor.close()
        cnx.close()
        return result
