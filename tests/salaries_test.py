import unittest
from nose.tools import *
from decimal import Decimal
from resuelvefc.salaries import *
from resuelvefc.exceptions import *

class SalariesTest(unittest.TestCase):

    def setUp(self):
        player1 =    {
            "nombre": "Juan Perez",
            "nivel": "C",
            "goles": 10,
            "sueldo": 50000,
            "bono": 25000,
            "sueldo_completo": None,
            "equipo": "rojo"
        }
        player2 = {
            "nombre": "EL Cuauh",
            "nivel": "Cuauh",
            "goles": 30,
            "sueldo": 100000,
            "bono": 30000,
            "sueldo_completo": None,
            "equipo": "azul"
        }
        player3 = {
            "nombre": "Cosme Fulanito",
            "nivel": "A",
            "goles": 7,
            "sueldo": 20000,
            "bono": 10000,
            "sueldo_completo": None,
            "equipo": "azul"
        }
        player4 =    {
            "nombre": "El Rulo",
            "nivel": "B",
            "goles": 9,
            "sueldo": 30000,
            "bono": 15000,
            "sueldo_completo": None,
            "equipo": "rojo"
        }
        self.original_input = [ player1,
                                player2,
                                player3,
                                player4 ]
        self.salaries = Salaries(self.original_input)


    def test_exceeded_team_rate(self):
        """Assert that the team rate cannot go above 1"""
        self.salaries.team_scored['chivas'] = 20
        self.salaries.team_goal['chivas'] = 10
        rate = self.salaries.team_rating('chivas')
        self.assertEqual(Decimal(1), rate)


    def test_team_rate(self):
        """Assert a correct team rate calculation"""
        self.salaries.team_scored['chivas'] = 10
        self.salaries.team_goal['chivas'] = 20
        rate = self.salaries.team_rating('chivas')
        self.assertEqual(Decimal(0.5), rate)


    def test_exceeded_player_rate(self):
        """Assert that the player rate cannot go above 1"""
        player = {
                'goles': 100,
                'goles_minimos': 10
                }
        rate = self.salaries.player_rating(player)
        self.assertEqual(Decimal(1), rate)


    def test_player_rate(self):
        """Assert a correct player rate calculus"""
        player = {
                'goles': 10,
                'goles_minimos': 100
                }
        rate = self.salaries.player_rating(player)
        self.assertEqual(Decimal('0.1'), rate)


    @raises(LevelNotFoundException)
    def test_a_non_existing_level(self):
        """Assert that we raise when we find a non existing level"""
        player = {
            "nombre": "El Rulo",
            "nivel": "non_existing_level",
            "goles": 9,
            "sueldo": 30000,
            "bono": 15000,
            "sueldo_completo": None,
            "equipo": "rojo"
        }
        salary = Salaries([player])
        salary.process()


    def test_player_levels(self):
        """Assert that we process correctly the goals per level"""
        result = self.salaries.process()
        self.assertEqual(result[0]['goles_minimos'], 15)
        self.assertEqual(result[1]['goles_minimos'], 20)
        self.assertEqual(result[2]['goles_minimos'], 5)
        self.assertEqual(result[3]['goles_minimos'], 10)


    def test_teams_count(self):
        """Assert that we count correctly the number of teams"""
        result = self.salaries.process()
        self.assertEqual(len(self.salaries.team_goal), 2)
        self.assertEqual(len(self.salaries.team_scored), 2)


    def test_teams_processing(self):
        """Assert that we process correctly the team grouping"""
        result = self.salaries.process()
        self.assertEqual(self.salaries.team_goal['azul'], 25)
        self.assertEqual(self.salaries.team_goal['rojo'], 25)
        self.assertEqual(self.salaries.team_scored['azul'], 37)
        self.assertEqual(self.salaries.team_scored['rojo'], 19)


    def test_stuff_that_should_remain(self):
        """Assert that we are not modifying anything that we shouldn't"""
        result_list = self.salaries.process()
        key_list = ['nombre', 'nivel', 'goles', 'sueldo', 'bono', 'equipo']

        for origin, result in zip(self.original_input, result_list):
            for key in key_list:
                self.assertEqual(origin[key], result[key])


    def test_correct_final_result(self):
        """Assert that we are processing correctly a final salary"""
        result_list = self.salaries.process()

        self.assertEqual(result_list[0]['sueldo_completo'],
                         Decimal('67833.33'))
        self.assertEqual(result_list[1]['sueldo_completo'],
                         Decimal('130000.00'))
        self.assertEqual(result_list[2]['sueldo_completo'],
                         Decimal('30000.00'))
        self.assertEqual(result_list[3]['sueldo_completo'],
                         Decimal('42450.00'))



if __name__ == '__main__':
    unittest.main()
