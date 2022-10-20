import requests
import json
from requests_toolbelt import MultipartEncoder

data = {"app_id": "","app_secret": ""} #更换机器人时更改
def get_tenant(data):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    res = requests.post(url=url, data=json.dumps(data))
    tenant = json.loads(res.content.decode())
    return tenant['tenant_access_token']  


def send(text, id):                                #mode open_id/chat_id
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type":""}
    if id[1] == 'u':
        params["receive_id_type"] = 'open_id'
    elif id[1] == 'c':
        params["receive_id_type"] = 'chat_id'
    msgContent = {
        "text": "",
    }
    msgContent["text"] = str(text)
    req = {
        "receive_id": id, 
        "msg_type": "text",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': "Bearer "+get_tenant(data), # your access token bearer xxx
        'Content-Type': 'application/json'
    }
    print(headers['Authorization'])
    response = requests.post(url=url, params=params, headers=headers, data=payload)
    print(response.headers['X-Tt-Logid']) # for debug or oncall
    print(response.content) # Print Response


def uploadImage(pic_path):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open(pic_path, 'rb'))}  # 需要替换具体的path 
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer xxx',  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Authorization'] = "Bearer " + get_tenant(data)
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    return json.loads(response.content)['data']["image_key"]

def sendImage(pic_path, id):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    params = {"receive_id_type":""}
    if id[1] == 'u':
        params["receive_id_type"] = 'open_id'
    elif id[1] == 'c':
        params["receive_id_type"] = 'chat_id'
    #print(params["receive_id_type"])
    msgContent = {
        "tag": "img","image_key": ""
    }
    msgContent["image_key"] = uploadImage(pic_path)
    req = {
        "receive_id": str(id), 
        "msg_type": "image",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': "Bearer "+get_tenant(data), # your access token bearer xxx
        'Content-Type': 'application/json'
    }
    response = requests.post(url=url, params=params, headers=headers, data=payload)
    print(response.headers['X-Tt-Logid']) # for debug or oncall
    print(response.content) # Print Response
