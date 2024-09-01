from re import fullmatch
import uuid
from datetime import datetime
from typing import Optional, override

from django_utils_morriswa.exceptions import ValidationException
from django_utils_morriswa.models import DataModel
from django_utils_morriswa.str_tools import isBlank


# settings
USER_SESSION_PLAYER_NAME_MIN_LEN = 4
USER_SESSION_PLAYER_NAME_MAX_LEN = 32
USER_SESSION_PLAYER_NAME_REGEXP = '^[A-Za-z0-9-_.]*$'
USER_SESSION_NUM_SHIPS_OPTIONS = ['1', '2', '3', '4', '5']


class UserSession(DataModel):

    def __init__(self, data: dict):
        self.session_id: Optional[uuid] = data.get('session_id')
        self.player_id: Optional[str] = data.get('player_id')
        self.player_name: str = data.get('player_name')
        self.num_ships: str = data.get('num_ships')
        self.session_started: Optional[datetime] = data.get('session_started')
        self.session_used: Optional[datetime] = data.get('session_used')

        if self.player_name is None or isBlank(self.player_name):
            raise ValidationException(field='player_name', error='required')

        if self.num_ships is None or isBlank(self.num_ships):
            raise ValidationException(field='num_ships', error='required')

        self.validate()

    @override
    def validate(self):

        if len(self.player_name) < USER_SESSION_PLAYER_NAME_MIN_LEN:
            raise ValidationException(field='player_name', error=f'min len {USER_SESSION_PLAYER_NAME_MIN_LEN}')
        elif len(self.player_name) > USER_SESSION_PLAYER_NAME_MAX_LEN:
            raise ValidationException(field='player_name', error=f'max len {USER_SESSION_PLAYER_NAME_MAX_LEN}')
        elif not fullmatch(USER_SESSION_PLAYER_NAME_REGEXP, self.player_name):
            raise ValidationException(field='player_name', error='A-Z a-z 0-9 - _ . only')

        if self.num_ships not in USER_SESSION_NUM_SHIPS_OPTIONS:
            raise ValidationException('num_ships', f'options: {USER_SESSION_NUM_SHIPS_OPTIONS}')

    @override
    def copy(self, data: dict): pass

    @override
    def json(self): pass
