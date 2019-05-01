import simplejson as json
from decimal import *
from resuelvefc.exceptions import *

class InputValidator(object):

    def __init__(self, in_json):
        self.in_json = in_json
        self.expected_types = self.get_expected_types()

    def encode(self):
        self.data = json.loads(self.in_json, use_decimal=True)

        self.validate_is_a_list()
        for player in self.data:
            self.validate_player(player)

        return self.data

    def validate_is_a_list(self):

        if( not isinstance(self.data, list) ):
            raise ArrayExpectedException()

        if( len(self.data) <= 0 ):
            raise ZeroPlayersReceivedException()

    def validate_player(self, player):

        if( not isinstance(player, dict)):
            raise InvalidPlayerFormatException()

        self.validate_player_fields(player)
        for key in self.expected_types:
            self.validate_player_field_format(player, key)

    def validate_player_fields(self, player):
        received_fields_set = set(player.keys())
        expected_fields_set = set(self.expected_types.keys())

        missing_fields = expected_fields_set - received_fields_set
        if( len(missing_fields) > 0 ):
            raise MissingFieldsException(str(list(missing_fields)))

        remaining_fields = received_fields_set - expected_fields_set
        if( len(remaining_fields) > 0 ):
            raise NonValidFieldsException(str(list(remaining_fields)))

    def validate_player_field_format(self, player, key):
        if( not key in player ):
            raise MissingFieldsException(key)

        value = player[key]
        expected_type_set = self.expected_types[key]
        if( not isinstance(value, expected_type_set) ):
            raise InvalidDataTypeFormatException(key + " - " + str(expected_type_set))


    def get_expected_types(self):
        return {
            'nombre': tuple([str]),
            'nivel' : tuple([str]),
            'goles' : tuple([int]),
            'sueldo': tuple([int, Decimal]),
            'bono'  : tuple([int, Decimal]),
            'sueldo_completo': tuple([type(None)]), # NoneType does not exist
            'equipo': tuple([str])
        }
