import requests
import os
from colorama import Fore, Style, init  
import json
import hashlib
from retrying import retry

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

#登录
@retry
def login():
	print("登录流程执行中…")
	userName=input("账号")
	password=input("密码")
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

#下载文件
def download(url,file_name):
	response=requests.get(url,stream=True)
	#print(response)
	current_dir = os.getcwd() 
	path = os.path.join(current_dir, file_name) 
	with open(path,'wb') as file:
		for chunk in response.iter_content(chunk_size=8192):
			file.write(chunk)

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
	#print(resourceList)
	print(len(resourceList))
	for o in range(0,len(resourceList)):
		homework_url=resourceList[o]['resourceUrl']
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

#获取作业类型
def homeworktype_get():
	typeget_1=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus/getTime?homeworkId="+homeworkId+"&studentId="+studentId+"&unitId="+unitId)
	typeget_2=typeget_1.text
	#print(typeget_2)
	homeworkStatu=json.loads(typeget_2).get('homeworkStatu')  
	typeget=homeworkStatu['homeworkType']
	#print(typeget)
	return typeget

#菜单部分
#qqq="https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList?studentId=9542C48DB599476E8F6020BB9DBF80B6&subjectCode=&homeworkType=-1&pageIndex=1&pageSize=0&statu=1&homeworkName=&unitId=9D12C13E97394EBFAB1489DAD98D8F02"
#qqq_1=requests.get(qqq)
#qqq_2 = qqq_1.text 
#print(qqq_2)
#qqq_3 = json.loads(qqq_2).get('homeworkNum') 
#print(qqq_3)
logo()
id=login()
studentId=id[0]
unitId=id[1]
homeworklist(studentId,unitId)
homeworkId=input("请输入作业ID:")
typeget=homeworktype_get()
if typeget==5:
	type5(homeworkId)
else:
	print(typeget)
	print("暂不支持，敬请期待")	
