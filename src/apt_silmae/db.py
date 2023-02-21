# import
import sqlite3
from dataclasses import astuple
from datetime import datetime
from .resource.region_code import region_code_dict

# definition
_TABLENAME_DATA = 'APT_SILMAE_DATA'
_TABLENAME_DATA_META = 'APT_SILMAE_DATA_META'
_TABLENAME_GEOCOORD = 'APT_SILMAE_GEOCOORD'
_TABLENAME_MAP = 'APT_SILMAE_MAP'


_QUERY_CREATETABLE_DATA = f"CREATE TABLE IF NOT EXISTS {_TABLENAME_DATA}(\
                            ID                INTEGER NOT NULL\
                                CONSTRAINT {_TABLENAME_DATA}_pk\
                                    PRIMARY KEY,\
                            PRICE             INTEGER unsigned,\
                            CONSTRUCTION_DATE char(8),\
                            TRADE_DATE        char(8),\
                            NET_LEASABLE_AREA FLOAT unsigned,\
                            REGION_CODE       INTEGER unsigned,\
                            DONG              TEXT,\
                            JIBUN             TEXT,\
                            APT               TEXT\
                        )"
_QUERY_CREATEINDEX_DATA = f"CREATE UNIQUE INDEX IF NOT EXISTS uindex\
                        on {_TABLENAME_DATA} (PRICE, CONSTRUCTION_DATE, TRADE_DATE, NET_LEASABLE_AREA, REGION_CODE, DONG, JIBUN, APT)"
_QUERY_INSERT_DATA = f"INSERT OR IGNORE INTO {_TABLENAME_DATA}(PRICE, CONSTRUCTION_DATE, TRADE_DATE, NET_LEASABLE_AREA, \
                    REGION_CODE, DONG, JIBUN, APT)\
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
_QUERY_CREATETABLE_DATA_META = f"CREATE TABLE IF NOT EXISTS {_TABLENAME_DATA_META}(\
                            ID                INTEGER NOT NULL\
                                CONSTRAINT {_TABLENAME_DATA_META}_pk\
                                    PRIMARY KEY AUTOINCREMENT,\
                            REGION_CODE       INTEGER unsigned,\
                            LAST_UPDATE_DATE  TEXT\
                        )"
_QUERY_INSERT_DATA_META = f"INSERT INTO {_TABLENAME_DATA_META}(REGION_CODE, LAST_UPDATE_DATE) VALUES (?, ?)"
_QUERY_UPDATE_DATA_META = f"UPDATE {_TABLENAME_DATA_META} SET LAST_UPDATE_DATE = ? WHERE REGION_CODE = ?"
_QUERY_SELECT_DATA_META = f"SELECT LAST_UPDATE_DATE FROM {_TABLENAME_DATA_META} WHERE REGION_CODE = ?"

_QUERY_CREATETABLE_GEOCOORD = f"CREATE TABLE IF NOT EXISTS {_TABLENAME_GEOCOORD}(\
                            ID                INTEGER NOT NULL\
                                CONSTRAINT {_TABLENAME_GEOCOORD}_pk\
                                    PRIMARY KEY,\
                            REGION_CODE   INTEGER unsigned,\
                            ADDRESS       TEXT,\
                            X  INTEGER,\
                            Y  INTEGER\
                        )"
_QUERY_INSERT_GEOCOORD = f"INSERT OR IGNORE INTO {_TABLENAME_GEOCOORD}(REGION_CODE, ADDRESS, X, Y) VALUES (?, ?, ?, ?)"
_QUERY_CREATEINDEX_GEOCOORD = f"CREATE UNIQUE INDEX IF NOT EXISTS APT_SILMAE_GEOCOORD_index\
                        on {_TABLENAME_GEOCOORD} (REGION_CODE, ADDRESS)"
_QUERY_SELECT_GEOCOORD = f"SELECT X, Y FROM {_TABLENAME_GEOCOORD} WHERE REGION_CODE = ? AND ADDRESS = ?"
_QUERY_SELECT_NOTIN_GEOCOORD = f"SELECT DISTINCT DONG || ' ' || JIBUN\
                                 FROM {_TABLENAME_DATA}\
                                 WHERE DONG || ' ' || JIBUN NOT IN (\
                                    SELECT ADDRESS\
                                    FROM APT_SILMAE_GEOCOORD\
                                 )\
                                AND REGION_CODE = ?"
_QUERY_CREATETABLE_MAP = f"CREATE TABLE IF NOT EXISTS {_TABLENAME_MAP}(\
                            ID                INTEGER NOT NULL\
                                CONSTRAINT {_TABLENAME_MAP}_pk\
                                    PRIMARY KEY,\
                            LEVEL   INTEGER unsigned,\
                            YYYY   INTEGER unsigned,\
                            MM   INTEGER unsigned,\
                            X  INTEGER,\
                            Y  INTEGER,\
                            WEIGHT  INTEGER unsigned,\
                            DESC  TEXT\
                        )"
_QUERY_DROP_MAP = f"DROP TABLE {_TABLENAME_MAP}"
_QUERY_INSERT_MAP = f"INSERT INTO {_TABLENAME_MAP}(LEVEL, YYYY, MM, X, Y, WEIGHT, DESC) VALUES (?, ?, ?, ?, ?, ?, ?)"
_QUERY_SELECT_COMPILE_SOURCE = f"SELECT a.REGION_CODE, a.PRICE, a.TRADE_DATE, a.NET_LEASABLE_AREA, b.X, b.Y, a.APT\
                                FROM {_TABLENAME_DATA} a,\
                                    {_TABLENAME_GEOCOORD} b\
                                WHERE a.REGION_CODE = ?\
                                AND a.REGION_CODE = b.REGION_CODE\
                                AND a.DONG || ' ' || a.JIBUN = b.ADDRESS"
_QUERY_SELECT_MAP_BY_DATE = f"SELECT LEVEL, YYYY, MM, X, Y, WEIGHT, DESC\
                                FROM {_TABLENAME_MAP}\
                                WHERE YYYY = ?\
                                AND MM = ?"



# initialize
print("[INFO] Initialize Start Database On apt_silmae")
connect = sqlite3.connect('db.sqlite3', check_same_thread=False)
connect.cursor().execute(_QUERY_CREATETABLE_DATA)
connect.cursor().execute(_QUERY_CREATEINDEX_DATA)
connect.cursor().execute(_QUERY_CREATETABLE_DATA_META)
connect.cursor().execute(_QUERY_CREATETABLE_GEOCOORD)
connect.cursor().execute(_QUERY_CREATEINDEX_GEOCOORD)
connect.cursor().execute(_QUERY_CREATETABLE_MAP)
print("[INFO] Initialize End Database On apt_silmae")

# method
def insert_data(datas):
    cursor = connect.cursor()
    for data in datas:
        cursor.execute(_QUERY_INSERT_DATA, astuple(data))
    connect.commit()
    cursor.close()


def insert_data_meta(region_code, update_date_time):
    cursor = connect.cursor()
    parameter = (region_code, update_date_time,)
    cursor.execute(_QUERY_INSERT_DATA_META, parameter)
    connect.commit()
    cursor.close()


def update_data_meta(region_code, **kwargs):
    # Decide update time
    if kwargs.get('time') is None:
        update_date_time = datetime.now().strftime('%Y%m%d %H:%M:%S')
    else:
        update_date_time = kwargs.get('time')

    # Decide insert or update
    if select_data_meta(region_code) is None:
        insert_data_meta(region_code, update_date_time)
    else:
        cursor = connect.cursor()
        parameter = (update_date_time, region_code,)
        cursor.execute(_QUERY_UPDATE_DATA_META, parameter)
        connect.commit()
        cursor.close()


def select_data_meta(region_code):
    cursor = connect.cursor()
    parameter = (region_code,)
    row = cursor.execute(_QUERY_SELECT_DATA_META, parameter).fetchone()
    cursor.close()
    return row[0] if row is not None else None


def select_geocoord(juso: str): # TODO
    cursor = connect.cursor()
    parameter = (juso,)
    row = cursor.execute(_QUERY_SELECT_GEOCOORD, parameter).fetchone()
    cursor.close()
    return row[0] if row is not None else None


def select_notingeocoord(region_code: int):
    cursor = connect.cursor()
    parameter = (region_code, )
    row = cursor.execute(_QUERY_SELECT_NOTIN_GEOCOORD, parameter).fetchall()
    cursor.close()
    return row if row is not None else None


def insert_geocoord(region_code, address, x, y):
    cursor = connect.cursor()
    parameter = (region_code, address, x, y, )
    cursor.execute(_QUERY_INSERT_GEOCOORD, parameter)
    connect.commit()
    cursor.close()


def select_compile_source(region_code: int):
    cursor = connect.cursor()
    parameter = (region_code, )
    row = cursor.execute(_QUERY_SELECT_COMPILE_SOURCE, parameter).fetchall()
    cursor.close()
    return row if row is not None else None


def reset_map_table():
    cursor = connect.cursor()
    cursor.execute(_QUERY_DROP_MAP)
    cursor.execute(_QUERY_CREATETABLE_MAP)
    connect.commit()
    cursor.close()


def insert_map(level, yyyy, mm, x, y, weight, desc):
    cursor = connect.cursor()
    parameter = (level, yyyy, x, y, weight, desc, )
    cursor.execute(_QUERY_INSERT_MAP, parameter)
    connect.commit()
    cursor.close()


def insert_map_list(map_list):
    cursor = connect.cursor()
    for map in map_list:
        parameter = (map[0], map[1], map[2], map[3], map[4], map[5], '', )
        cursor.execute(_QUERY_INSERT_MAP, parameter)
    connect.commit()
    cursor.close()


def select_map_by_date(yyyy, mm):
    cursor = connect.cursor()
    parameter = (yyyy, mm, )
    row = cursor.execute(_QUERY_SELECT_MAP_BY_DATE, parameter).fetchall()
    cursor.close()
    return row if row is not None else None
