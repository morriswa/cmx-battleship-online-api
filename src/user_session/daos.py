import logging
import uuid
import datetime
from typing import Optional

from django.db import IntegrityError
from app.exceptions import BadRequestException, APIException

from app import connections
from user_session.models import LoginRequest, AuthenticatedPlayer


def retrieve_session(session_id: uuid) -> Optional[AuthenticatedPlayer]:
    """ retrieves user session from session_id """
    with connections.cursor() as db:
        # retrieve player data if session is not timed out
        db.execute("""
            select * 
            from user_session
            where 
                session_id = %s 
                and session_used between NOW() - INTERVAL '10 MINUTES' and NOW()
        """, (session_id,))
        player_data = db.fetchone()

        if player_data is None:
            return None
        else:
            player = AuthenticatedPlayer(player_data)
            # if session is found and valid, update timestamp in the database
            db.execute("""update user_session set session_used = current_timestamp where session_id = %s """, (session_id,))
            # and return
            return player

def get_online_player_count() -> int:
    count: int
    with connections.cursor() as db:
        db.execute("""
            -- delete unused rows
            delete from user_session where session_used not between NOW() - INTERVAL '10 MINUTES' AND NOW();
            -- and count remaining players
            select count(player_id) as online_player_count from player_slot where in_use = 'Y';
        """)
        count = db.fetchone().get('online_player_count') or 0

    return count

def get_available_player_id() -> str:
    """ retrieves next available player id from database """
    player_id: str
    with connections.cursor() as db:
        db.execute("select player_id from player_slot where in_use = 'N' limit 1")
        result = db.fetchone()
        player_id = result.get('player_id')
        if result is None or player_id is None:
            raise APIException("Failed to retrieve available player id, is the server full?")

    return player_id


def start_session(session: LoginRequest) -> dict:
    """ Start Session Function
        We will declare gen_session_id as a uuid
        We will declare a gen_player_id as a string

        We connect to the db, as we are connected, we will generate a random uuid and call the get_available_player id for respective variables declared.
        Now, we will insert into the user_session table values of (session_id, player_id, player_name, num_ships) 
        
        If it works, we display a log of the successfully started session and return the session and player ids
        If it doesn't work, we will display the error message.
    """ 
    try:
        gen_session_id: uuid
        gen_player_id: str
        with connections.cursor() as db:
            gen_session_id = uuid.uuid4()
            gen_player_id = get_available_player_id()

            db.execute("""
                insert into user_session (session_id, player_id, player_name, num_ships)
                values (%s, %s, %s, %s)
            """, (gen_session_id, gen_player_id, session.player_name, session.num_ships))

        logging.info(f"Successfully started session {gen_session_id} for {session.player_name}#{gen_player_id}")

        return {
            'session_id': gen_session_id,
            'player_id': gen_player_id
        }
    except Exception as e:
        logging.error('error on start_session', e)


def end_session(session_id: uuid) -> None:
    """ 
        Ending session function

        In this function, we connect to the db 
        If we can find the session_id, we delete it from the user_session table with the session_id given in the params of this function.

        If it works, we log that the session was safely terminated and return which session it was
        If it doesn't work, we log the error and try to debug. 
"""
    try:
        with connections.cursor() as db:
            db.execute("""
                delete from user_session where session_id = %s;
            """, (session_id,))

        logging.info(f"Safely terminated session {session_id}")
    except Exception as e:
        logging.error('error on end_session', e)
