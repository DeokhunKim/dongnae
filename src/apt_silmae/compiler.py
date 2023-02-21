from . import db
from src.apt_silmae.config import config
from collections import defaultdict

_config = config['LEVEL_INFO']


def test():
    source = db.select_compile_source(11110)
    for i in source:
        x = i[4]
        y = i[5]
        print(x)
        print(y)


def compile_do(source):
    for level in _config['LEVEL_LIST']:
        print(f"[INFO] + + compiler level {level}")
        compile_level(source, level, coord_shift=_config['COORD_SHIFT'][level])


def compile_level(source, level, coord_shift):
    # Collection by shifted location
    rows = defaultdict(list)
    for point in source:
        x = (point[4] >> coord_shift) << coord_shift
        y = (point[5] >> coord_shift) << coord_shift
        rows[(x, y, 'Y', point[2][:4])].append((int(point[1]/point[3]), point[6]))
        rows[(x, y, 'M', point[2][:4]+point[2][4:6])].append((int(point[1]/point[3]), point[6]))

    result = []
    for row in rows:
        apt_dict = defaultdict(list)
        all_place_sum = 0
        for place in rows[row]:
            apt_dict[place[1]].append(place[0])
            all_place_sum += place[0]
        avg = round( all_place_sum / len(rows[row]) ) if len(rows[row]) != 0 else 0
        desc = ''
        for apt in apt_dict:
            desc += f"{apt}: {sum(apt_dict[apt]) / len(apt_dict[apt])} \n"
        # level, YYYY, MM, x, y, avg_price, desc
        #result.append((level, row[2], row[3], row[0], row[1], avg, desc))
        result.append((level, row[3][:4], '' if row[2] == 'Y' else row[3][4:6], row[0], row[1], avg))
    db.insert_map_list(result)








