import urllib
import urllib.request
import re

def download_page(url):
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	data = response.read()
	return data

def get_image(html):
	regx = r'(images[\S]*\.(jpg|png))'
	pattern = re.compile(regx)
	get_img = re.findall(pattern,repr(html))
	print (get_img)
	num = 1
	for img in get_img:
		image = download_page('http://www.yuhuadong.me:8080/c2c/'+img[0])
		with open ('%s.jpg'%num,'wb') as fp:
			fp.write(image)
			num += 1
	return
def get_one_image(url):
	request = urllib.request.Request(url)
	response = urllib.request.urlopen(request)
	get_img = response.read()
	with open('1.jpg','wb') as fp:
		fp.write(get_img)
		print('图片下载完成')
	return
# html = 'images/goods/b2ab433c4f6311e794be52540007a88f.jpg images/goods/b2ab433c4f6311e794be52540007a88f.jpg'
# regx = r'(images[\S]*\.(jpg|png))'
# pattern = re.compile(regx)
# get_img = re.findall(pattern,repr(html))
# print(get_img[0])
url = 'http://www.yuhuadong.me:8080/c2c/listGoods.do'
html = download_page(url)
get_image(html)