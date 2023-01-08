import sqlite3
import logging

from tg_bot.config_reader import config
from tg_bot.db.db_interface import Database

db = Database(name=config.db.get_secret_value())
db_logger = logging.getLogger('db')


def unblock_user_db(user_id):
    try:
        db.execute('UPDATE user SET is_blocked = ?  WHERE user_id = ?', (False, user_id,))
    except sqlite3.Error as err:
        db_logger.info(err)
        return False
    finally:
        db.commit()
        return True


def db_insert_id(user_id):
    try:
        db.execute("INSERT or IGNORE INTO user(user_id) VALUES(?)", (user_id,))
    except sqlite3.Error as err:
        db_logger.info(f'number already exists {err}')
    finally:
        db.commit()


def db_insert_phone(user_id, user_phone):
    try:
        db.execute("INSERT INTO phone(user_id, phone_number) VALUES(?, ?)", (user_id, user_phone,))
    except sqlite3.Error as err:
        db_logger.info(f'number already exists {err}')
    finally:
        db.commit()


def db_user_block_update(user_id):
    try:
        db.execute('UPDATE user SET is_blocked = ?  WHERE user_id = ?', (True, user_id,))
    except sqlite3.Error as err:
        db_logger.info(err)
    finally:
        db.commit()


def db_select_blocked(user_id):
    try:
        db.execute('SELECT is_blocked FROM user WHERE user_id = ?', (user_id,))
    except sqlite3.Error as err:
        db_logger.info(err)
    finally:
        return db.fetchone()

