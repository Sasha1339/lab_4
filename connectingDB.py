import sqlite3

class ConnectingDB:

    def first_connect(self, query1, query2):
        try:
            connection = sqlite3.connect('test_to_lab4')
            cursor = connection.cursor()

            cursor.execute(query1)
            cursor.execute(query2)
            #record = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("ошибка", error)
        finally:
            if connection:
                connection.close()
                #print("Соединение успешно разорвано")


    def create_query(self, query):
        try:
            connection = sqlite3.connect('test_to_lab4')
            cursor = connection.cursor()

            cursor.execute(query)
            connection.commit()
            #record = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("ошибка", error)
        finally:
            if connection:
                connection.close()
                #print("Соединение успешно разорвано")

    def create_query_return(self, query):
        try:
            connection = sqlite3.connect('test_to_lab4')
            cursor = connection.cursor()
            cursor.execute(query)
            record = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("ошибка", error)
        finally:
            if connection:
                connection.close()
                #print("Соединение успешно разорвано")
        return record