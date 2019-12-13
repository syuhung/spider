from bs4 import BeautifulSoup
import os
import requests

if __name__ == '__main__':

	#所要爬取的小说的目录页，要修改时只需要修改网址即可
	target_url = 'https://www.biqubao.com/book/26212'
	#本地保存路径
	save_path = './novel'
	#小说网站的根目录
	index_path = 'https://www.biqubao.com'

	req = requests.get(url = target_url, verify = False)

	req.encoding = 'gbk'

	soup = BeautifulSoup(req.text, features='html.parser')

	list_tag = soup.div(id='list')

	story_tag = list_tag[0].dl.dd.string

	dir_path = os.path.join(save_path, story_tag)

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	for dd_tag in list_tag[0].dl.find_all('dd'):
		#章节名称
		chapter_name = dd_tag.string
		#章节地址
		chapter_url = index_path + dd_tag.a.get('href')
		#访问章节地址，并爬取正文部分
		chapter_req = requests.get(url = chapter_url)
		chapter_req.encoding = 'gbk'
		chapter_soup = BeautifulSoup(chapter_req.text, 'html.parser')
		#解析正文所在标签
		content_tag = chapter_soup.div.find(id='content')
		#获取正文内容，并将空格替换为换行
		content_text = str(content_tag.text.replace('\xa0', '\n'))
		#讲文本写入本地文件并以章节命名
		with open(os.path.join(dir_path, chapter_name) + '.txt', 'w') as f:
			f.write('本章地址：' + chapter_url)
			f.write(content_text)