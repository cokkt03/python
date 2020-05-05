"""
CYCO
作者:Ren
日期:2020/05/05
功能:水資源物聯網感測作業平台與Webaccess連接，將流量計上傳至水資源物聯網


"""


import random
import json  
import datetime 
import time
import requests
import tkinter as tk
#Webaccess Headers
headers = {
    'Content-Type' : 'application/json; charset=utf-8; LoginType=view;',
    'Authorization' : 'Basic YWRtaW4'
}

#水利署headers
token_url = "https://iapi.wra.gov.tw/v3/oauth2/token"
payload_id = 'grant_type=client_credentials&client_id=MSGjrh6JrOO/5AbG1v88je/KIFkIeDOsjZWi25UcxIg%3D&client_secret=bRj2WMeCfnJTwWkVTkvJoQ%3D%3D'
headers_token = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'cookiesession1=167C34E3HHVONHNDKNDMEUMGPPV66C5D'
}
response = requests.request("GET", token_url, headers=headers_token, data = payload_id)
get_token=response.text.encode('utf8')
jget_token=json.loads(get_token)
print(jget_token,type(jget_token))

#取得token
data_token=jget_token['access_token']
data_token_type=jget_token['token_type']
data_Authorization=data_token_type+' '+data_token
print(data_token)
print(data_token_type)
print(data_Authorization)

#Webaccess登入
url_Log="http://localhost/WaWebService/JSON/Login"
r = requests.get(url_Log, auth=('admin',''))
print(r.status_code)
print(r.text.encode('utf8'))

#取得數值
url_TagValue='http://localhost/WaWebService/Json/GetTagValue/JAES-Water'
r2 = requests.post(url_TagValue, headers = headers, auth=('admin',''), json={"Tags":[{"Name":"Rain_Acc_Flow" }]} )
tag=r2.text.encode('utf8')
json_TagValue=json.loads(tag)
tag1=json_TagValue["Values"]
print(tag1)
clist=tag1
for tag2 in clist:
    print(tag2)
get_tag=tag2["Value"]

#抓取系統時間
url_ServerTime='http://localhost/WaWebService/Json/ServerTime'
r1 = requests.get(url_ServerTime,headers = headers,auth=('admin',''))
json_sertime=json.loads(r1.text)
json_date=json_sertime["Date"]
json_time=json_sertime["Time"]
transfer_time=json_date+' '+json_time+'+08:00'


#資料格式整理
data={}
data["Id"]="cee21132-f1bf-44d8-a1f8-8b77bbd24fd0"
data["Timestamp"]=transfer_time
data["Value"]=get_tag
data["ValueStatus"]=1
json_data=json.dumps(data)
print(json_data)
upload_data="[\t"+json_data+"\t]"
print(upload_data,type(upload_data))


#送出資料
upload_url = "https://iapi.wra.gov.tw/v3/api/TimeSeriesData/write"
headers = {
  'Authorization': data_Authorization,
  'Content-Type': 'text/plain',
  'Cookie': 'cookiesession1=167C34E3HHVONHNDKNDMEUMGPPV66C5D'
}
response = requests.request("POST", upload_url, headers=headers, data =upload_data)
print(response.text.encode('utf8'))



### app視窗
app=tk.Tk()
app.title('App Upload')     #視窗名稱
app.geometry('400x300')     #視窗大小
app.resizable(0,0)          #固定視窗大小
#app.iconify()              #視窗最小化 

app.mainloop()



#
url_Log="http://localhost/WaWebService/JSON/Login"
r = requests.get(url_Log, auth=('admin',''))
print(r.status_code)
print(r.text)
#
url_ServerTime='http://localhost/WaWebService/Json/ServerTime'
r1 = requests.get(url_ServerTime,headers = headers,auth=('admin',''))
print(r1.status_code)
print(r1.text)
#
url_TagValue='http://localhost/WaWebService/Json/GetTagValue/JAES-Water'
r2 = requests.post(url_TagValue, headers = headers, auth=('admin',''), json={"Tags":[{"Name":"Rain_Acc_Flow" }]} )
print(r2.status_code)
print(r2.text)
#
url_alarm='http://localhost/WaWebService/Json/GetVersion/JAES-Water'
r3 = requests.get(url_alarm,headers = headers,auth=('admin',''))
print(r3.status_code)
print(r3.text)
"""
