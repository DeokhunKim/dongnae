import math

from . import struct
from . import downloader
from .resource.region_code import region_code_dict
from . import db
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from . import juso_geocoord
from . import compiler

# Method
def update_all_region_data() -> str:
    print(f"[INFO] Update All Region Data Start")
    for region_code in region_code_dict:
        try:
            update_region_data(region_code)
        except Exception as e:
            print(e)
            break
    print(f"[INFO] Update All Region Data End")
    return


def update_region_data(region_code: int) -> str:
    print(f"[INFO] Update Region - {region_code}")
    # Check last update date
    last_update_time = db.select_data_meta(region_code)
    if last_update_time is None:
        last_update_time = '20150101'
    else:
        last_update_time = last_update_time[:8]
    current_time = datetime.now().strftime('%Y%m%d')
    if int(current_time) == int(last_update_time):
        return None

    # Download database
    s_timedelta = date(int(last_update_time[0:4]), int(last_update_time[4:6]), int(last_update_time[6:8]))
    while int(s_timedelta.strftime('%Y%m')) <= int(datetime.now().strftime('%Y%m')):
        deal_ymd = s_timedelta.strftime('%Y%m')
        db.insert_data(
            downloader.download_data(region_code=region_code, deal_ymd=int(deal_ymd))
        )
        # next month
        s_timedelta = s_timedelta + relativedelta(months=1)

    # Save DB
    db.update_data_meta(region_code)
    return


def update_geocoord():
    print('[INFO] Update Geocoord Start')
    for region_code in region_code_dict:
        print(f"[INFO] - update {region_code}..")
        rows = db.select_notingeocoord(region_code)
        for row in rows:
            juso = f"{region_code_dict[region_code]} {row[0]}"
            coord = juso_geocoord.reqeust_coord_by_juso(juso)
            if coord is None:
                continue
            x = math.floor(float(coord['x']) * 10000000)
            y = math.floor(float(coord['y']) * 10000000)
            db.insert_geocoord(region_code, address=row[0], x=x, y=y)
    print('[INFO] Update Geocoord End')


def recompile_all_region():
    print('[INFO] Recompile All Region Start')
    print('[INFO] + reset map table')
    db.reset_map_table()
    for region_code in region_code_dict:
        print(f"[INFO] + compiler region {region_code}")
        compiler.compile_do(
            db.select_compile_source(region_code)
        )
    print('[INFO] Recompile All Region End')


def get_map_by_date(yyyy, mm):
    return db.select_map_by_date(yyyy, mm)


