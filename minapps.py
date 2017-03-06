import urllib.request
import json
import os

def getData(api_url):
    # set data
    hjson = getHjson(api_url)
    minapps = hjson['data']['rows']
    return minapps

# get icon $ img
def getMinapp(minapps, dir_path, qr1, qr2):
	dirpath = getDirPath(dir_path)

	for minapp in minapps:
		printName(minapp['title'],minapp['content'])
		saveList(dirpath, minapp['title'], minapp['content'])
		minapp_path = getDirPath(dirpath+'/'+minapp['title'])+'/'

	if(minapp['qrcode'] == STATIC_QR):
	    saveQr_Code(MINA_QR, minapp_path, minapp['title'])
	else:
	    saveQr_Code(minapp['qrcode'], minapp_path, minapp['title'])

	saveText(minapp_path, minapp['title'], minapp['content'])
	getIcon(minapp['icon'], minapp_path, minapp['title'])
	getAttr_Img(minapp['attr_imgs'], minapp_path, minapp['title'])

def printName(title,content):
	print('---------------'+'\n'
	    	+title+'\n'
	    	+content+'\n'
	    	+'---------------') 

# 返回 json 数据
def getHjson(api_url):
    url = api_url
    url_data = urllib.request.urlopen(url).read().decode()
    return json.loads(url_data)

def saveQr_Code(url, path, title):
    saveImg(url, path, title+'_二维码_')

# 写入二进制数据
def saveImg(url, path, title):
    with open(path+title+'.jpg', 'wb') as file:
        req = urllib.request.urlopen(url)
        buf = req.read()
        file.write(buf)
        file.flush()

def saveList(path, title, content):
    with open(path+'/'+'小程序'+'.txt', 'a', encoding='utf-8') as file:
        file.writelines(title+'\n'+content+'\n'+'-------------'+'\n')
        file.flush()

# 写入文本
def saveText(path, title, content):
    with open(path+title+'.txt', 'w', encoding='utf-8') as file:
        file.writelines(title+'\n'+content+'\n')
        file.flush()

# 获得单个小程序的本地文件地址
def getDirPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# 获得小程序的Icon
def getIcon(icon_url, path, title):
    saveImg(icon_url, path, title+'_icon_')

# 获得图片
def getAttr_Img(attr_img_urls, path, title):
    i = 0
    attr_img_urls_list = attr_img_urls.split(',')
    for attr_img_url in attr_img_urls_list:
        saveImg(attr_img_url, path, title+'_attr_%s' % str(i))
        i = i + 1

n = 1
API_URL = 'http://9.cn/Xcx/Index/getAppList?page='+str(n)+'&code=&status=1&order=create_time+DESC'
DIR_PATH = '/Users/atree/Desktop/9cn'
STATIC_QR = '/static/common/images/default_qrcode.png'
MINA_QR = 'https://media.ifanrusercontent.com/media/user_files/trochili/dd/2c/dd2c51444f2edd3c863a8f2671072c8f6f44633e-4892369f4bd44762ae3eef4d8897a5025ac65ad5.jpg'

getMinapp(getData(API_URL),DIR_PATH,STATIC_QR,MINA_QR)
