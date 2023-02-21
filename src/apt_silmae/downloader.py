import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.apt_silmae.config import config
from .struct import ApiData
import requests
import xml.etree.ElementTree as xml

_config = config['APT_SILMAEMAE_DOWNLOAD']


def download_data(region_code: int, deal_ymd: int):
    result = []
    resp = requests.get(f"{_config['REQUEST_URL']}?"
                        f"serviceKey={_config['SERVICEKEY']}"
                        f"&LAWD_CD={region_code}"
                        f"&DEAL_YMD={deal_ymd}")
    root = xml.fromstring(resp.text)
    result_code = root.find('header').find('resultCode').text
    if result_code == '99':  # over limit request
        raise Exception('[INFO] Request limit exceeded. Close the program.')

    body = root.find('body')
    if body is None:
        return result
    items = body.find('items')
    for item in items:
        try:
            data = ApiData(
                item.find('거래금액').text.replace(",", "").strip(),
                item.find('건축년도').text,
                f"{item.find('년').text}{item.find('월').text.zfill(2)}{item.find('일').text.zfill(2)}",
                item.find('전용면적').text,
                item.find('지역코드').text,
                item.find('법정동').text.strip(),
                item.find('지번').text,
                item.find('아파트').text
            )
            result.append(data)
        except AttributeError:
            continue

    return result