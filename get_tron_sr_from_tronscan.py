#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:26:46 2019

@author: ale.liu

Get Tron-SR info

"""

import requests
import xlwt
import xlrd

# ---------------------------需要修改---------------------------------
# --------------------------base_data-------------------------------
#Tron-sr url             
tron_sr_base_url = "https://apilist.tronscan.org/api/witness"

#基础数据文件（之前统计的SR信息）
tron_sr_info_path = "local_tron_sr_info_path"
save_new_tron_sr_fiel_path = "new_tron_sr_info_path"


#add browser headers
headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie':'__cfduid=da90fabee5f4d96a316a104f96f0476bd1552904746; gtm_session_first=Mon%20Mar%2018%202019%2018:24:58%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); _ga=GA1.2.1809757759.1552904698; _gid=GA1.2.1536504574.1552904698; _fbp=fb.1.1552904698688.846897282; __gads=ID=df0e159e39a6f1bc:T=1552904750:S=ALNI_Mb2GRbqU9zQCWB8Lc_nA4QIsEBTjw; cmc_gdpr_hide=1; gtm_session_last=Mon%20Mar%2018%202019%2020:24:30%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4); _awl=2.1552911928.0.4-68ecec8c-3d6c2c480ef438cc86a4fd41099005f0-6763652d75732d7765737431-5c8f8e38-0'
}


#get base_tron_sr_info from local file
def read_base_tron_sr_info(tron_sr_info_path):
    read_tron_sr_info_file =  xlrd.open_workbook(tron_sr_info_path)
    tron_sr_data_from_base_data = read_tron_sr_info_file.sheet_by_name("Sheet1")
    return tron_sr_data_from_base_data
    



#get content form tronscan
def get_tron_sr_info_from_tronscan(tron_sr_base_url):
    tron_sr_form_tronscan_content = list(requests.get(tron_sr_base_url,headers=headers).json())
    tron_sr_form_tronscan_list = tron_sr_form_tronscan_content[0:27]
    return tron_sr_form_tronscan_list

    

# write new tron sr to local file
def write_new_tron_sr_info_to_file(tron_sr_form_tronscan_list,tron_sr_data_from_base_data,save_new_tron_sr_fiel_path):
    write_tron_sr_file = xlwt.Workbook()
    sheet1 = write_tron_sr_file.add_sheet('tron_sr_from_tronscan')
    sheet1.write(0,0,"排名")
    sheet1.write(0,1,'SR名称')
    sheet1.write(0,2,"渠道")
    sheet1.write(0,3,'群名')
    sheet1.write(0,4,"升级是否")
    sheet1.write(0,5,'IP')
    sheet1.write(0,6,"机器配置")
    sheet1.write(0,7,'机器所在位置')
    tron_sr_list_from_base_data = tron_sr_data_from_base_data.col_values(1)[1:]
    #转换为小写
    tron_sr_list_from_base_data_lower  = [tron_sr_name.lower() for tron_sr_name in tron_sr_list_from_base_data]
    
    for i in range(27):
        print(i+1,"-------正在写入",tron_sr_form_tronscan_list[i]['name'],"--------------")
        if tron_sr_form_tronscan_list[i]['name']=='':
            tron_sr_form_tronscan_list[i]['name'] = tron_sr_form_tronscan_list[i]['url']
        sheet1.write(i+1,0,i+1)
        sheet1.write(i+1,1,tron_sr_form_tronscan_list[i]['name'])
        if tron_sr_form_tronscan_list[i]['name'].lower() in tron_sr_list_from_base_data_lower:
            for k in range(len(tron_sr_list_from_base_data)):
                #获取对应tron-sr的微信，机器配置，ip等信息      
                if tron_sr_form_tronscan_list[i]['name'].lower() == tron_sr_data_from_base_data.row_values(k)[1:][0].lower():
                    print(tron_sr_data_from_base_data.row_values(k)[1])
                    content = tron_sr_data_from_base_data.row_values(k)[2:]
                    #写入tron-sr对应的信息
                    for j in range(len(content)):
                        sheet1.write(i+1,j+2,content[j])
    write_tron_sr_file.save(save_new_tron_sr_fiel_path)


def main():
    tron_sr_data_from_base_data = read_base_tron_sr_info(tron_sr_info_path)
    tron_sr_form_tronscan_list = get_tron_sr_info_from_tronscan(tron_sr_base_url)
    write_new_tron_sr_info_to_file(tron_sr_form_tronscan_list,tron_sr_data_from_base_data,save_new_tron_sr_fiel_path)
    
      

if (__name__ == "__main__"):
    main()
