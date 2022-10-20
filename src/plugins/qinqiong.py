import requests
import os
from .supersender import *
def planar(id, d=''):
    
    # 定义图片的保存路径，url.split('=')[-1]的意思是截取图片链接中最后一个=后的字符为图片名字
    path=d+str(id)+'.jpg'

    # 判断目录是否存在，如果不存在建立目录
    if not os.path.exists(d):
        os.mkdir(d)
    # 通过requests.get获得图片
    url = 'http://localhost:11451/api/QRGuard/'+ str(id)[3:23] +'/code'
    r=requests.get(url)
    r.raise_for_status()
    # 打开要存储的文件，然后将r.content返回的内容写入文件中，因为图片是二进制格式，所以用‘wb’，写完内容后关闭文件，提示图片保存成功
    with open(path,'wb') as f:
        f.write(r.content)
        f.close()
        print("保存成功")
    
    sendImage(path, id)

