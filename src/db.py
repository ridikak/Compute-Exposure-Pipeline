import sqlite3
from .config import CFG

def connect():
    return sqlite3.connect(CFG["db_path"])
