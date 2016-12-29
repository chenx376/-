from urllib.request import urlopen
from bs4 import BeautifulSoup
import data,re,os
import csv,ast,decimal

# from root page to find all the urls we need
html=data.data
Qiche_Obj=BeautifulSoup(html,'html.parser')
carIndexs=Qiche_Obj.find_all('div',{'class':'uibox','id':re.compile('box[A-Z]'),'style':''})
urls=[]
for i in range(len(carIndexs)):
	carName_1=carIndexs[i]
	carName_2=carName_1.find_all('h4')
	for j in range(len(carName_2)):
		car_url_all=carName_2[j].find('a')
		car_url_noCont=carName_2[j].find('a',{'class':'greylink'})
		if car_url_noCont==None:
			urls.append(car_url_all['href'])


# get into the next page 
for url in urls:
	html=urlopen(url)
	bsObj=BeautifulSoup(html,'html.parser')

	#get into the parameters page
	index=bsObj.find_all('li',{'class':'nav-item'})
	index=index[1]
	index=index.find('a')
	if index==None:
		continue
	url2=index['href']

	page=urlopen(url2).read()
	page_utf=page.decode('gbk')
	bsObj=BeautifulSoup(page_utf,'html.parser')


	#get csv name and open a csv file
	csv_filepath=os.getcwd()
	csv_filepath=os.path.join(csv_filepath,'csv')
	title=bsObj.find('title')
	title=title.contents[0]
	title=title[3:]
	csv_filepath=os.path.join(csv_filepath,title+'.csv')
	csv_file=open(csv_filepath,'w',newline='')
	csv_write=csv.writer(csv_file)



	#get contents 
	index=bsObj.find('script',{'type':'text/javascript','src':'http://x.autoimg.cn/car/config/series/library.js'})
	index=index.next_sibling
	index=index.next_sibling
	content=index.contents
	content=str(content)


	#make contents
	content=re.findall('var config.*var option',content)
	content=re.findall('config.*\}\]\}\]\}\]\}\}\;',content[0])


	content=content[0].replace('config = ','')
	content=content.replace(';','')
	content=content.replace('null','None')
	content=ast.literal_eval(content)


	rawname=content["result"]['paramtypeitems']
	for k in range(len(rawname)):
		allname=rawname[k]['paramitems']
		for j in range(len(allname)):
			name=allname[j]
			content_write=[]
			item_name=name['name']
			content_write.append(item_name)
			for i in range(len(name)):
				name_value=name['valueitems']
				for z in name_value:
					content_write.append(z['value'])
			csv_write.writerow(content_write)
	csv_file.close()

