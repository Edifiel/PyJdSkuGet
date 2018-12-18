# coding=utf8

import sys
import os
from SqlHelper import Sqlite, SafeInput
from config import *
from bs4 import BeautifulSoup as bs
import requests
import time
import random
import json

rootPath = os.getcwd()

def read_cate_to_db():
    """
    读取京东类别并保存到数据库
    :return:
    """
    cate_url = "https://www.jd.com/allSort.aspx"
    cate_response = get_http_response(cate_url)
    if cate_response.status_code == 200:
        cate_values = []
        # html.parser, lxml, xml, html5lib
		bs_obj = bs(cate_response.text, 'html.parser')
        box_list = bs_obj.select('div.category-item')
        for box in box_list:
            root_span = box.select_one("span")
            print(root_span)
            if root_span is None or root_span.text != "手机":
                continue
            print(box)
            root_name = root_span.text
            dl_list = box.select("dl.clearfix")
            for dl in dl_list:
                link_list = dl.select("a")
                if len(link_list) == 0:
                    continue
                second_name = link_list[0].text
                for link in link_list[1:]:
                    url = link.attrs["href"]
                    third_name = link.text
                    cid = int(url[url.rfind(",") + 1:])
                    cate_values.append({"cid": cid,
										"root_name": root_name,
										"second_name": second_name,
										"cname": third_name,
										"curl": "https:" + url})
        if len(cate_values) > 0:
            sqlite_conn = SqliteHelper()
            sqlite_conn.exec_many_no_query("INSERT INTO %s(cid,root_name,second_name,cname,curl) " % cate_tb_name +
										   "VALUES(:cid, :root_name, :second_name, :cname, :curl)", cate_values)
        print("read cate over")
        return
    print("cate read error,code=", cate_response.status_code)


if __name__ == '__main__':
	read_cate_to_db()
    """
    cateid = sys.argv[1] if len(sys.argv) > 1 else 7
    page = sys.argv[2] if len(sys.argv) > 2 else 1
    try:
        read_cate_for_down_list(cateid, page)
    except Exception, ex:
        print(ex)

	try:
		read_no_images_item()
	except Exception as ex:
	    print(ex)
    """
