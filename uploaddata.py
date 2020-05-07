"""
CYCO
作者:Ren
日期:2020/05/05
功能:水資源物聯網感測作業平台與Webaccess連接，將流量計上傳至水資源物聯網

"""

import json  
import requests
import tkinter as tk
import time

print('Start Upload Data...')
#Webaccess Headers
headers = {
    'Content-Type' : 'application/json; charset=utf-8; LoginType=view;',
    'Authorization' : 'Basic YWRtaW4'
}

#水利署headers
token_url = "https://iapi.wra.gov.tw/v3/oauth2/token"
#輸入client_id=  client_secret=
payload_id = 'grant_type=client_credentials&client_id=******&client_secret=******'
headers_token = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'cookiesession1=167C34E3HHVONHNDKNDMEUMGPPV66C5D'
}

response_token = requests.request("GET", token_url, headers=headers_token, data = payload_id)
get_token=response_token.text.encode('utf8')
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
if get_tag <= 0:
    get_tag=0

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

t=time.time()
local_time = time.ctime(t)
print(local_time)
time_result = time.localtime(t)
#
print('Done')
### app視窗
app=tk.Tk()
app.title('App Upload')     #視窗名稱
app.geometry('400x300')     #視窗大小
app.resizable(0,0)          #固定視窗大小
label_time = tk.Label(app,text = time_result)
label_time.pack()
label_resopnse = tk.Label(app,text = json.loads(response.text)["DetailMessage"])
label_resopnse.pack()

def destoryApp():
  print('Destory')
  app.destroy()
  return 0

destory_App=destoryApp()
app.mainloop()

