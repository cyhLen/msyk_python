import requests
import os
from colorama import Fore, Style, init  
import json
import hashlib
from retrying import retry

################基础功能函数###############

#字符转md5函数
def string_to_md5(string):
	md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
	return md5_val

#打印彩色logo
def logo():  
    blue = Fore.CYAN  
    string = """
__nnn__nnn____ __n_nnnnnnnnnn ___n_____n__n_ n___nnnnnnnnnn
nnnnnnnnnnnnnn __n_____nn____ __nn_____n____ _n__n___nn___n
____nnnn______ __n_nnnnnnnnnn _n_n_nnnnnnnnn ____nnnnnnnnnn
nnnnnnnnnnnnnn n_n_n___nn___n n__n_____n____ nn__n___nn___n
____nnnn______ n_n_n___nn___n ___n____nnn___ _n__nnnnnnnnnn
nnnnnnnnnnnnnn n_n_n___nn___n ___n___n___n__ _n______nn____
____nnnn______ n_n_n___nn___n ___n___n___n__ _n__nnnnnnnnnn
nnnnnnnnnnnnnn n_n_n___nn___n ___n__n____n__ _n_____nnnn___
____nnnn______ n_n_n___nn___n ___n__n____n__ _n____n_nn_n__
___nnnnnn_____ __n_n___nn___n ___n__n____n__ _n___n__nn__n_
__nnn__nnn____ _n__n___nn___n ___n_n_____n_n _nn_n___nn___n
_nnn____nnn___ _n______nn____ ___n_n_____nnn _n__n___nn___n"  """
    for char in string:  
        if char == 'n':  
            print(f"{blue}{char}{Style.RESET_ALL}", end='')  
        else:  
            print(char, end='')  
    print(Style.RESET_ALL) 

#下载文件
def download(url,file_name):
	response=requests.get(url,stream=True)
	#print(response)
	current_dir = os.getcwd() 
	path = os.path.join(current_dir, file_name) 
	with open(path,'wb') as file:
		for chunk in response.iter_content(chunk_size=8192):
			file.write(chunk)

#最新推出的基础功能函数！！！不要错过！
#url源文件提取url，加前辍并遍历输出，询问是否下载(源文件为包含url的最低一级列表)
def url_deal_and_download(analysistList):
	if len(analysistList)!=0:
		for o in range(0,len(analysistList)):
			resourceUrl_material=analysistList[o]['resourceUrl']
			title=analysistList[o]['title']
			print("文件名:",title)
			#print(resourceUrl_material)
			for w in resourceUrl_material:
				if str(resourceUrl_material).lower().startswith('http'):
					file_url=resourceUrl_material
				elif str(resourceUrl_material).lower().startswith('//'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_material
				elif str(resourceUrl_material).lower().startswith('/'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_material
				else:
					file_url="https://msyk.wpstatic.cn/"+resourceUrl_material
			print(file_url)
			download_choose=input("是否要下载该文件？[Y/n]")
			if download_choose=='Y' or download_choose=='y':
				download(file_url,analysistList[o]['title'])
			else:
				q=1
	else:
		print("无文件")

################登录部分###############

#登录
@retry
def login():
	print("登录流程执行中…")
	userName=input("账号  ")
	password=input("密码  ")
	pwd=string_to_md5(userName+password+"HHOO")
	loginurl='https://padapp.msyk.cn/ws/app/padLogin?userName='+userName+'&auth='+pwd
	login_get = requests.get(loginurl)
	login_first = login_get.text 
	login_last = json.loads(login_first).get('InfoMap') 
	message=json.loads(login_first).get('message')
	if login_last is None:
		print(message)
		#login()
	else:
		print("登录成功!")
		#print(login_last)
		print("姓名:",login_last['realName'],"学校:",login_last['schoolName'],"班级:",login_last['groupName'],"学号",login_last['studentNumber'])
	unitId=login_last["unitId"]
	studentId=login_last["id"]
	return studentId,unitId

################作业获取部分################

#获取作业列表并输出
def homeworklist(studentId,unitId):
	num_1=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList?studentId="+studentId+"&subjectCode=&homeworkType=-1&pageIndex=1&pageSize=0&statu=1&homeworkName=&unitId="+unitId)
	num_2=num_1.text
	#print(num_2)
	homeworkNum=json.loads(num_2).get('homeworkNum') 
	list_1=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList?studentId="+studentId+"&subjectCode=&homeworkType=-1&pageIndex=1&pageSize="+str(homeworkNum)+"&statu=1&homeworkName=&unitId="+unitId)
	list_2=list_1.text
	#print(list_2)
	homeworkNum=json.loads(list_2).get('homeworkNum') 
	sqHomeworkDtoList=json.loads(list_2).get('sqHomeworkDtoList') 
	#homework1=sqHomeworkDtoList[0]
	#print(homework1['id'],"作业类型:",homework1['homeworkType'],homework1['homeworkName'])
	#homeworkNum=int(homeworkNum)
	#print(len(sqHomeworkDtoList))
	print("新作业:",homeworkNum,"已开始:",len(sqHomeworkDtoList))
	for i in range(0,len(sqHomeworkDtoList)):
		homework_i=sqHomeworkDtoList[i]
		print(homework_i['id'],"作业类型:",homework_i['homeworkType'],"[",homework_i['subjectName'],"]",homework_i['homeworkName'])

#阅读材料类作业获取
def type5(homeworkid):
	read_1=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus?homeworkId="+homeworkid+"&modifyNum=0&userId="+studentId+"&unitId="+unitId)
	read_2=read_1.text
	#print(read_2)
	resourceList = json.loads(read_2).get('resourceList')  
	homeworkName= json.loads(read_2).get('homeworkName') 
	print("作业名称:",homeworkName)
	#print(resourceList)
	print("文件个数:",len(resourceList))
	for o in range(0,len(resourceList)):
		homework_url=resourceList[o]['resourceUrl']
		resTitle=resourceList[o]['resTitle']
		print("文件名:",resTitle)
		#print(homework_url)
		for w in homework_url:
			if str(homework_url).lower().startswith('http'):
				file_url=homework_url
			elif str(homework_url).lower().startswith('//'):
				file_url="https://msyk.wpstatic.cn"+homework_url
			elif str(homework_url).lower().startswith('/'):
				file_url="https://msyk.wpstatic.cn"+homework_url
			else:
				file_url="https://msyk.wpstatic.cn/"+homework_url
		print(file_url)
		download_choose=input("是否要下载文件？[Y/n]")
		if download_choose=='Y' or download_choose=='y':
			download(file_url,resourceList[o]['resTitle'])
		else:
			q=1
	return homework_url

#答题卡类作业获取
def type7(homeworkId):
	read_1=requests.get("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo?homeworkId="+homeworkId+"&studentId="+studentId+"&modifyNum=0&unitId="+unitId)
	read_2=read_1.text
	#print(read_2)
	analysistList=json.loads(read_2).get('analysistList') 
	materialRelas=json.loads(read_2).get('materialRelas') 
	#print(analysistList)
	#resourceUrl_material=analysistList[0]['resourceUrl']
	#resourceUrl_answer=materialRelas[0]['resourceUrl']
	#print(resourceUrl_material)
	#print(resourceUrl_answer)
	homeworkName= json.loads(read_2).get('homeworkName') 
	print("作业名称:",homeworkName)

	#beta

	if len(analysistList)!=0:
		for o in range(0,len(analysistList)):
			resourceUrl_material=analysistList[o]['resourceUrl']
			title=analysistList[o]['title']
			print("文件名:",title)
			#print(resourceUrl_material)
			for w in resourceUrl_material:
				if str(resourceUrl_material).lower().startswith('http'):
					file_url=resourceUrl_material
				elif str(resourceUrl_material).lower().startswith('//'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_material
				elif str(resourceUrl_material).lower().startswith('/'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_material
				else:
					file_url="https://msyk.wpstatic.cn/"+resourceUrl_material
			print(file_url)
			download_choose=input("是否要下载该答案文件？[Y/n]")
			if download_choose=='Y' or download_choose=='y':
				download(file_url,analysistList[o]['title'])
			else:
				q=1
	else:
		print("无答案文件")

	if len(materialRelas)!=0:
		for o in range(0,len(materialRelas)):
			resourceUrl_answer=materialRelas[o]['resourceUrl']
			title=materialRelas[o]['title']
			print("文件名:",title)
			#print(resourceUrl_answer)
			for w in resourceUrl_answer:
				if str(resourceUrl_answer).lower().startswith('http'):
					file_url=resourceUrl_answer
				elif str(resourceUrl_answer).lower().startswith('//'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_answer
				elif str(resourceUrl_answer).lower().startswith('/'):
					file_url="https://msyk.wpstatic.cn"+resourceUrl_answer
				else:
					file_url="https://msyk.wpstatic.cn/"+resourceUrl_answer
			print(file_url)
			download_choose=input("是否要下载该材料文件？[Y/n]")
			if download_choose=='Y' or download_choose=='y':
				download(file_url,materialRelas[o]['title'])
			else:
				q=1
		#return resourceUrl_material,resourceUrl_answer
	else:
		print("无材料文件")

#获取作业类型
def homeworktype_get(homeworkId):
	typeget_1=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus/getTime?homeworkId="+homeworkId+"&studentId="+studentId+"&unitId="+unitId)
	typeget_2=typeget_1.text
	#print(typeget_2)
	homeworkStatu=json.loads(typeget_2).get('homeworkStatu')  
	typeget=homeworkStatu['homeworkType']
	#print(typeget)
	return typeget

#作业答案部分
def get_homework():
	homeworkId=input("请输入作业ID:")
	typeget=homeworktype_get(homeworkId)
	if typeget==5:
		type5(homeworkId)
	elif typeget==7:
		type7(homeworkId)
	else:
		print(typeget)
		print("暂不支持，敬请期待")

###############消息获取部分#################

#打印消息列表
def informationlist():
	pagenum=1
	inflistget_1=requests.get("https://msgapp.msyk.cn/ws/student/information/informationListForStudent?userId="+studentId+"&type=0&pageSize=20&pageIndex="+str(pagenum)+"&startTime=&endTime=&exigencyType=&subjectCodes=&title=&accessory=0")
	inflistget_2=inflistget_1.text
	#print(inflistget_2)
	data= json.loads(inflistget_2).get('data') 
	#print(data)
	informationList=data['informationList']
	#print(informationList[0])
	uuid_list=[]
	for inf_order in range(0,len(informationList)):
		i=inf_order+1
		uuid=informationList[inf_order]['uuid']
		globals()[f'global_var_{i}'] = uuid
		#uuid_is=f'global_var_{i}'
		uuid_list.append(uuid)
		#print(uuid_list)
		print("序号:",i,"发送者:",informationList[inf_order]['sendUserName'],"标题:",informationList[inf_order]['title'])
		print(informationList[inf_order]['content'])

	informationget(uuid_list)

#获取消息详情
def informationget(uuid_list):
	#print(uuid_list)
	uuid_num1=input("请输入序号")
	uuid_num2=int(uuid_num1)-1
	uuid_inf=uuid_list[uuid_num2]
	infget_1=requests.get("https://msgapp.msyk.cn/ws/teacher/information/getInformationDetail?userId="+studentId+"&unitId="+unitId+"&uuid="+uuid_inf+"&drafts=false")
	infget_2=infget_1.text
	print(infget_2)
	data= json.loads(infget_2).get('data') 
	accessoryList=data['information']['accessoryList']
	contentUrl=data['information']['contentUrl']
	contentUrl_list=[]
	contentUrl_dict={}
	contentUrl_dict['title']='title'
	contentUrl_dict['resourceUrl']=contentUrl
	contentUrl_list.append(contentUrl_dict)
	url_deal_and_download(contentUrl_list)
	url_deal_and_download(accessoryList)

##################主菜单部分################

#循环菜单
def menu():
	do_it=input("请输入需要执行的任务:\n1.作业答案获取\n2.查看消息(开发中)3.跑作业id(开发中)\n4.(开发中)\n")
	while True:
		if int(do_it)==1:
			get_homework()
			do_it=input("请输入需要执行的任务:\n1.作业答案获取\n2.查看消息(开发中)3.跑作业id(开发中)\n4.(开发中)\n")
		elif int(do_it)==2:
			informationlist()
			do_it=input("请输入需要执行的任务:\n1.作业答案获取\n2.查看消息(开发中)3.跑作业id(开发中)\n4.(开发中)\n")
		elif int(do_it)==3:
			q=1
		else:
			get_homework()
			do_it=input("请输入需要执行的任务:\n1.作业答案获取\n2.查看消息(开发中)3.跑作业id(开发中)\n4.(开发中)\n")
			

#程序主体
logo()
id=login()
studentId=id[0]
unitId=id[1]
homeworklist(studentId,unitId)
menu()