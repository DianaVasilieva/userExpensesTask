import unittest
import database


class Test_insert_rows(unittest.TestCase):

    def test_statistic_date_day(self):
        connection = database.connect()
        res = database.get_date_statistic_day(connection, '01', '01', '2023')
        correct_res = [('clothes', 3445)]
        self.assertEqual(correct_res, res)

    def test_statistic_date_month(self):
        connection = database.connect()
        res = database.get_date_statistic_month(connection, '11', '2022')
        correct_res = [('food', 2345), ('clothes', 3245)]
        self.assertEqual(correct_res, res)

    def test_statistic_date_year(self):
        connection = database.connect()
        res = database.get_date_statistic_year(connection, '2022')
        correct_res = [('food', 2345), ('clothes', 3245), ('households', 4668)]
        self.assertEqual(correct_res, res)

    def test_statistic_date_day_user(self):
        connection = database.connect()
        res = database.get_date_statistic_with_user_day(connection, 1, '01', '01', '2023')
        correct_res = [('clothes', 3445)]
        self.assertEqual(correct_res, res)

    def test_statistic_date_month_user(self):
        connection = database.connect()
        res = database.get_date_statistic_with_user_month(connection, 1, '11', '2022')
        correct_res = []
        self.assertEqual(correct_res, res)

    def test_statistic_date_year_user(self):
        connection = database.connect()
        res = database.get_date_statistic_with_user_year(connection, 2, '2022')
        correct_res = [('food', 2345), ('clothes', 3245)]
        self.assertEqual(correct_res, res)

    def test_category_statistic(self):
        connection = database.connect()
        res = database.get_category_statistic(connection, 'stationery')
        correct_res = [(234, '20', '01', '2023')]
        self.assertEqual(correct_res, res)


if __name__ == '__main__':
    unittest.main()
