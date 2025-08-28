from colorama import Fore, Style, init,Back
from PIL import Image as pilImage
import requests
import json
import hashlib
import time
import re
import os

import getHomeworkId_new
import homework_submit
################常量与常函数###############
init(autoreset=True)

serialNumbers,answers="",""
question_list = []

################基础功能函数###############
#发送post请求
def post(url, **params):
    try:
        response = requests.post(url, params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        print("网络连接失败，请检查代理设置")
        exit(1)

#字符转md5函数
def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

#文件转base64
def file_to_base64(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        encoded_content = base64.b64encode(content)
        base64_string = encoded_content.decode('utf-8')
        return base64_string
    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

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
_nnn____nnn___ _n______nn____ ___n_n_____nnn _n__n___nn___n  """
    for char in string:  
        if char == 'n':  
            print(f"{blue}{char}{Style.RESET_ALL}", end='')  
        else:  
            print(char, end='')  
    print(Style.RESET_ALL)

#下载文件
def download(url,file_name,*args):
    response=requests.get(url,stream=True)
    current_dir = os.getcwd() 
    path = os.path.join(current_dir, file_name) 
    if args:
        path=args[0]
    with open(path,'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

#(该函数计划删掉)
#最新推出的基础功能函数！！！不要错过！
#url源文件提取url，加前辍并遍历输出，询问是否下载(源文件为包含url的最低一级列表)
def url_deal_and_download(analysistList):
    if len(analysistList)!=0:
        for o in range(0,len(analysistList)):
            resourceUrl_material=analysistList[o]['resourceUrl']
            title=analysistList[o]['title']
            print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+title)
            #print(resourceUrl_material)
            for w in resourceUrl_material:
                file_url=url_deal("https://msyk.wpstatic.cn",resourceUrl_material)
            print(Fore.GREEN+file_url)
            download_choose=input(Fore.BLUE+"是否要下载该文件？[Y/n]")
            if download_choose=='Y' or download_choose=='y':
                download(file_url,analysistList[o]['title'])
                print(Fore.WHITE+"下载成功")
            else:
                print(Fore.WHITE+"已取消下载")
    else:
        input("无文件(按回车键继续)")

#该函数计划统一到此
def url_deal(head,resourceUrl_material):
    if str(resourceUrl_material).lower().startswith('http'):
        file_url=resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('//'):
        file_url=head+resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('/'):
        file_url=head+resourceUrl_material
    else:
        file_url=head+"/"+resourceUrl_material
    return file_url

#三个URL处理函数
def url_deal_inf(resourceUrl_material):
    if str(resourceUrl_material).lower().startswith('http'):
        file_url=resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('//'):
        file_url="https://msgapp.msyk.cn"+resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('/'):
        file_url="https://msgapp.msyk.cn"+resourceUrl_material
    else:
        file_url="https://msgapp.msyk.cn/"+resourceUrl_material
    return file_url

def url_deal_ava(resourceUrl_material):
    if str(resourceUrl_material).lower().startswith('http'):
        file_url=resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('//'):
        file_url="https://file.msyk.cn/store"+resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('/'):
        file_url="https://file.msyk.cn/store"+resourceUrl_material
    else:
        file_url="https://file.msyk.cn/store/"+resourceUrl_material
    return file_url

#十三位时间戳转换
def timestamp_to_date(timestamp):
    time_struct = time.localtime(timestamp/1000)
    time_standard = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
    return time_standard
    
#ppt下载
def ppt_download(pptResourceId,resTitle):
    ppt_list=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/homeworkPPTInfo?pptResourceId="+pptResourceId+"&resSource=1").text
    sqPptConvertList = json.loads(ppt_list).get('sqPptConvertList')
    print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+resTitle)
    download_choose=input(Fore.BLUE+"是否要下载该文件？[Y/n]")
    if download_choose=='Y' or download_choose=='y':
        current_dir = os.getcwd() 
        for page in range(len(sqPptConvertList)):
            path=sqPptConvertList[page]['path']
            pdfurl=url_deal("https://msyk.wpstatic.cn",path)
            print(pdfurl)
            displayNum=sqPptConvertList[page]['displayNum']
            pdfname=str(displayNum)+".jpg"
            path = os.path.join(current_dir,pptResourceId,pdfname) 
            os.makedirs(os.path.dirname(path), exist_ok=True)
            download(pdfurl,pdfname,path)
        convert_images_to_pdf(os.path.join(current_dir,pptResourceId),os.path.join(current_dir,resTitle))
        print(Fore.WHITE+"下载成功")
    else:
        print(Fore.WHITE+"已取消下载")

################pdf处理###############
#图片正则排序
def numeric_sort(value):
    digits = re.compile(r'(\d+)')
    parts = digits.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# 简易版——图片转换为pdf，pdf页面随图片大小浮动
def convert_images_to_pdf(image_file,output_path):
    print("正在转换为pdf")
    os.chdir(image_file)
    images = []
    file_lis = os.listdir(image_file)
    file_lis.sort(key=numeric_sort)
    output_path = output_path+'output.pdf'
    con = 0
    for image_path in file_lis:
        if image_path.endswith(('.jpg', '.png')):
            image = pilImage.open(image_path)
            images.append(image.convert("RGB"))
            con += 1
            print(image_path + '：第%d张' % con)
    images[0].save(output_path, save_all=True, append_images=images[1:])
    print('转换完成，共计%d张图片' % len(images))


################登录缓存###############
#来自msykanswer
def getAccountInform():
    ReturnInform=""
    ProfileImport=""
    try:
        for line in open("ProfileCache.txt", "r",encoding='utf-8').readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            ReturnInform = ReturnInform + line
        setAccountInform(ReturnInform)
        print("检测到 ProfileCache，尝试缓存登录中。（如失败自动执行登录流程）")
    except:
        print("未检测到 ProfileCache，执行登录流程。")
        ProfileImport=input(Fore.CYAN+"可提供未缓存的登录信息(失败则自动执行设备信息登录):")
        try:
            setAccountInform(ProfileImport)
        except:
            print(Fore.RED+"错误：登录信息有误或已经失效。")
            print(Fore.WHITE)
            loginMenu()

#获取账号信息(来自msykanswer)
def setAccountInform(result):
    #成功登录 获取账号信息
    if json.loads(result).get('code')=="10000":
        save_json(result,json.loads(result).get('InfoMap').get('realName'))
        open("ProfileCache.txt","w",encoding='utf-8').write(result)
        print("ProfileCache 登录缓存已更新。(下一次优先自动读取)")
        global unitId,id,studentId,userId,classId
        unitId=json.loads(result).get('InfoMap').get('unitId')
        id=json.loads(result).get('InfoMap').get('id')
        classId=json.loads(result).get('InfoMap').get('classId')
        studentId=id
        userId=studentId
    #登录失败 打印原因
    else:
        print(Fore.RED + json.loads(result).get('message'))
        exit(1)
#保存登录信息
def save_json(data,filename):
    filename+=".json"
    try:
        file = open(filename,'w')
        file.write(data)
        file.close
        print(Fore.MAGENTA + "保存登录信息成功 "+filename)
    except:
        print(Fore.RED + "保存登录信息失败")

################登录部分###############
def login():
    print(Fore.GREEN+"登录流程执行中…")
    while True:
        userName=input(Fore.CYAN+"账号  ")
        password=input("密码  ")
        pwd=string_to_md5(userName+password+"HHOO")
        loginurl='https://padapp.msyk.cn/ws/app/padLogin?userName='+userName+'&auth='+pwd
        login_first = requests.get(loginurl).text
        login_last = json.loads(login_first).get('InfoMap') 
        message=json.loads(login_first).get('message')
        if login_last is None:
            print(Fore.RED+message)
        else:
            print(Fore.MAGENTA+"登录成功!")
            #print(login_last)
            print(Back.WHITE+Fore.MAGENTA+"姓名:",login_last['realName'],Back.WHITE+Fore.MAGENTA+"学校:",login_last['schoolName'],Back.WHITE+Fore.MAGENTA+"班级:",login_last['groupName'],Back.WHITE+Fore.MAGENTA+"学号:",login_last['studentNumber'])
            global unitId,userId,studentId,id
            unitId=login_last["unitId"]
            studentId=login_last["id"]
            userId=studentId
            id=studentId
            setAccountInform(login_first)
            break

def loginMenu():
    loginway=input(Fore.RED+"请选择登录方式:\n"+Fore.MAGENTA+"1.ID登录\n2.账号密码登录"+Fore.WHITE)
    if loginway=="1":
        global unitId,studentId,userId
        print("提示:使用ID登录不会保存登录信息")
        unitId=input(Fore.CYAN+"请输入学校ID")
        studentId=input("请输入用户ID")
        userId=studentId
    elif loginway=="2":
        login()
    else:
        login()

################作业获取部分################

#获取作业列表并输出
def homeworklist(studentId,unitId):
    num_2=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList?studentId="+studentId+"&subjectCode=&homeworkType=-1&pageIndex=1&pageSize=0&statu=1&homeworkName=&unitId="+unitId).text
    homeworkNum=json.loads(num_2).get('homeworkNum') 
    list_2=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList?studentId="+studentId+"&subjectCode=&homeworkType=-1&pageIndex=1&pageSize="+str(homeworkNum)+"&statu=1&homeworkName=&unitId="+unitId).text
    #print(num_2,list_2)
    homeworkNum=json.loads(list_2).get('homeworkNum') 
    sqHomeworkDtoList=json.loads(list_2).get('sqHomeworkDtoList') 
    print(Fore.GREEN+"新作业:",Back.GREEN+str(homeworkNum),Fore.GREEN+"已开始:",Back.GREEN+str(len(sqHomeworkDtoList)))
    for i in range(0,len(sqHomeworkDtoList)):
        homework_i=sqHomeworkDtoList[i]
        print(Fore.YELLOW+str(homework_i['id']),Fore.YELLOW+"作业类型:",Fore.YELLOW+str(homework_i['homeworkType']),"[",Back.WHITE+Fore.MAGENTA+homework_i['subjectName'],"]",Fore.YELLOW+str(homework_i['homeworkName']))

#阅读材料类作业获取
def type5(homeworkid):
    read_2=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus?homeworkId="+homeworkid+"&modifyNum=0&userId="+studentId+"&unitId="+unitId).text
    #print(read_2)
    resourceList = json.loads(read_2).get('resourceList')  
    homeworkName= json.loads(read_2).get('homeworkName') 
    print(Fore.YELLOW+"作业名称:",Fore.MAGENTA+Back.WHITE+homeworkName)
    #print(resourceList)
    print(Fore.YELLOW+"文件个数:",len(resourceList))
    for o in range(0,len(resourceList)):
        resourceType=resourceList[o]['resourceType']
        #print(resourceType)
        if resourceType==5:
            homework_url=resourceList[o]['resourceUrl']
            resTitle=resourceList[o]['resTitle']
            ppt_download(homework_url,resTitle)
        else:
            homework_url=resourceList[o]['resourceUrl']
            resTitle=resourceList[o]['resTitle']
            print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+resTitle)
            file_url=url_deal("https://msyk.wpstatic.cn",homework_url)
            print(Fore.GREEN+file_url)
            download_choose=input(Fore.BLUE+"是否要下载文件？[Y/n]")
            if download_choose=='Y' or download_choose=='y':
                download(file_url,resourceList[o]['resTitle'])
                print(Fore.WHITE+"下载文件成功")
            else:
                print(Fore.WHITE+"已取消下载")

#答题卡类作业获取
def type7(homeworkId):
    read_2=requests.get("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo?homeworkId="+homeworkId+"&studentId="+studentId+"&modifyNum=0&unitId="+unitId).text
    #print(read_2)
    analysistList=json.loads(read_2).get('analysistList') 
    materialRelas=json.loads(read_2).get('materialRelas') 
    homeworkCardList=json.loads(read_2).get('homeworkCardList') 
    homeworkName= json.loads(read_2).get('homeworkName') 
    print("作业名称:",Fore.MAGENTA+Back.WHITE+homeworkName)
    operation_answerget(homeworkCardList,homeworkId)
    
    if len(analysistList)!=0:
        for o in range(0,len(analysistList)):
            resourceUrl_material=analysistList[o]['resourceUrl']
            title=analysistList[o]['title']
            print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+title)
            
            file_url=url_deal("https://msyk.wpstatic.cn",resourceUrl_material)
            print(Fore.GREEN+file_url)
            download_choose=input(Fore.BLUE+"是否要下载该答案文件？[Y/n]")
            if download_choose=='Y' or download_choose=='y':
                download(file_url,analysistList[o]['title'])
                print(Fore.WHITE+"下载文件成功")
            else:
                print(Fore.WHITE+"已取消下载")
    else:
        print(Fore.RED+"无答案文件")

    if len(materialRelas)!=0:
        for o in range(0,len(materialRelas)):
            resourceUrl_answer=materialRelas[o]['resourceUrl']
            title=materialRelas[o]['title']
            print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+title)
            
            file_url=url_deal("https://msyk.wpstatic.cn",resourceUrl_answer)
            print(Fore.GREEN+file_url)
            download_choose=input(Fore.BLUE+"是否要下载该材料文件？[Y/n]")
            if download_choose=='Y' or download_choose=='y':
                download(file_url,materialRelas[o]['title'])
                print(Fore.WHITE+"下载文件成功")
            else:
                print(Fore.WHITE+"已取消下载")
    else:
        print(Fore.RED+"无材料文件")

#获取作业类型
def homeworktype_get(homeworkId):
    typeget_2=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus/getTime?homeworkId="+homeworkId+"&studentId="+studentId+"&unitId="+unitId).text
    if "isWithdrawal" in typeget_2:
        return "isWithdrawal"
    else:
        homeworkStatu=json.loads(typeget_2).get('homeworkStatu')  
        typeget=homeworkStatu['homeworkType']
        return typeget

def get_homework():
    homeworkId=input(Fore.YELLOW+"请输入作业ID:")
    typeget=homeworktype_get(homeworkId)
    if typeget=="isWithdrawal":
        print(Fore.RED+"该作业不存在或被撤回或被删除")
    elif typeget==5:
        type5(homeworkId)
    elif typeget==7:
        type7(homeworkId)
    else:
        type7(homeworkId)

def operation_answerget(homeworkCardList,homeworkid):
    serialNumbers,answers="",""
    for num in range(0,len(homeworkCardList)):
        resourceId=homeworkCardList[num]['resourceId']
        orderNum=homeworkCardList[num]['orderNum']
        serialNumber=homeworkCardList[num]['serialNumber']
        url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+studentId+"&homeworkResourceId="+str(resourceId)+"&orderNum="+str(orderNum)+"&showAnswer=1&unitId="+unitId+"&modifyNum=1"
        html_doc=requests.get(url).text
        answer=ljlVink_parsemsyk(html_doc,str(orderNum),url)
        question_list.append(resourceId)
        
        if answer!="wtf":
            answer=(lambda answer: answer if len(answer) == 1 else ''.join('1' if char in answer else '0' for char in "ABCDEFGHIJ"))(answer)
            if serialNumbers=="":
                serialNumbers+=str(serialNumber)
                answers+=answer
            else:
                serialNumbers+=";"+str(serialNumber)
                answers+=";"+answer
    print(answers,serialNumbers)
    choose=input(Fore.BLUE+"是否提交选择答案[Y/n]:")
    if choose=="y" or choose=="Y":
        operation_answersubmit(answers,serialNumbers,homeworkid)
    else:
        print("已取消提交选择答案")

#页面提取选择答案(来自msykanswer)
def ljlVink_parsemsyk(html_doc,count,url):
    html_doc.replace('\n',"")
    index=html_doc.find("var questions = ")
    index1=html_doc.find("var resource")
    if index !=-1:
        data=json.loads(html_doc[index+16:index1-7])
        if data[0].get('answer')!=None:
            answer="".join(data[0].get('answer')).lstrip("[")[:-1].replace('"','').lstrip(",").replace(',',' ')
            if(re.search(r'\d', answer)):
                open_url(url)
                print(Fore.GREEN+count+" 在浏览器中打开")
                return "wtf"
            else:
                print(Fore.GREEN+count+" "+answer)
                return answer
        else:
            print(Fore.RED+count+" "+"没有检测到答案,有可能是主观题")
            return "wtf"

#选择题答案提交
def operation_answersubmit(answers,serialNumbers,homeworkId):
    submiturl="https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives?serialNumbers="+serialNumbers+"&answers="+answers+"&studentId="+studentId+"&homeworkId="+homeworkId+"&unitId="+unitId+"&modifyNum=0"
    #print(submiturl)
    print("自动提交选择答案中")
    a=requests.get(submiturl)
    check=homework_submit.answerSubmitCheck(studentId,unitId,homeworkId,answers)
    if check[0]==True:
        print("成功")
    else:
        print("提交失败，正在排查多选题问题")
        #print(check)
        homework_submit.resubmit(studentId,unitId,homeworkId,serialNumbers,check[1],answers)
        
    
#跑作业ID(来自msykanswer)
def getUnreleasedHWID():
    EndHWID=0
    StartHWID=int(input(Fore.YELLOW + "请输入起始作业id:"))
    EndHWID=int(input(Fore.YELLOW + "请输入截止作业id(小于起始则不会停):"))
    hwidplus100=StartHWID+100
    while True:
        if StartHWID==hwidplus100:
            print(Fore.GREEN+"已滚动100项 当前"+str(hwidplus100))
            hwidplus100+=100
        res=requests.get("https://padapp.msyk.cn/ws/common/homework/homeworkStatus?homeworkId="+str(StartHWID)+"&modifyNum=0&userId="+userId+"&unitId="+unitId).text
        if 'isWithdrawal' in res:
            pass
        else:
            hwname=json.loads(res).get('homeworkName')
            print(Fore.MAGENTA+str(StartHWID)+" "+hwname)
        
        if StartHWID==EndHWID:
            print(Fore.CYAN+"跑作业id结束 当前作业id为"+str(StartHWID))
            break
        StartHWID+=1

###############消息获取部分#################

#消息数量获取
def information_numget():
    infnumget_2=requests.get("https://msgapp.msyk.cn/ws/teacher/information/getInformationUnreadNum?userId="+studentId).text
    #print(infnumget_2)
    data= json.loads(infnumget_2).get('data') 
    print(Fore.WHITE+"新消息:",Fore.WHITE+str(data['num']))


#打印消息列表
def informationlist():
    pagenum=1
    while True:
        inflistget_2=requests.get("https://msgapp.msyk.cn/ws/student/information/informationListForStudent?userId="+studentId+"&type=0&pageSize=20&pageIndex="+str(pagenum)+"&startTime=&endTime=&exigencyType=&subjectCodes=&title=&accessory=0").text
        data= json.loads(inflistget_2).get('data') 
        informationList=data['informationList']
        #print(informationList[0])
        uuid_list=[]
        for inf_order in range(0,len(informationList)):
            i=inf_order+1
            uuid=informationList[inf_order]['uuid']
            globals()[f'global_var_{i}'] = uuid
            uuid_list.append(uuid)
            print(Fore.YELLOW+"序号:",Fore.YELLOW+str(i),Fore.YELLOW+"发送者:",Fore.YELLOW+informationList[inf_order]['sendUserName'],Fore.YELLOW+"标题:",Fore.YELLOW+informationList[inf_order]['title'])
            print(Fore.WHITE+informationList[inf_order]['content'])
        print(Fore.GREEN+"当前第",pagenum,Fore.GREEN+"页")
        cho=input(Fore.MAGENTA+"1.上一页\n2.查看详情\n3.下一页\n4.返回上一级\n"+Fore.RED+"请输入需要执行的任务:")
        cho=int(cho)
        if cho==1:
            pagenum-=1
        elif cho==3:
            pagenum+=1
        elif cho==2:
            informationget(uuid_list)
        elif cho==4:
            break
        else:
            pagenum=1

#获取消息详情
def informationget(uuid_list):
    uuid_num1=input(Fore.RED+"请输入序号")
    uuid_num2=int(uuid_num1)-1
    uuid_inf=uuid_list[uuid_num2]
    infget_2=requests.get("https://msgapp.msyk.cn/ws/teacher/information/getInformationDetail?userId="+studentId+"&unitId="+unitId+"&uuid="+uuid_inf+"&drafts=false").text
    #print(infget_2)
    data= json.loads(infget_2).get('data') 
    accessoryList=data['information']['accessoryList']
    print(Fore.MAGENTA+Back.WHITE+data['information']["title"])
    print(Fore.GREEN+"发送者: ",data['information']['sendUserName'])
    print(Fore.GREEN+"接收列表: \n","  ".join(str(value['realName']) for value in data['information']['recipientList']))
    contentUrl=url_deal("https://msg.msyk.cn",data['information']['contentUrl'])
    print(Fore.GREEN+contentUrl)
    download_choose=input(Fore.BLUE+"是否要下载消息内容？[Y/n]")
    if download_choose=='Y' or download_choose=='y':
        download(contentUrl,""+".html")
        print(Fore.WHITE+"下载文件成功")
    else:
        print(Fore.WHITE+"已取消下载")
    url_deal_and_download(accessoryList)

##################学习圈部分################
#学习圈菜单	
def questionmenu():
    teacherlist()
    question_privatelists=question_privatelist()
    #print(question_privatelists)
    ques_choice=input(Fore.MAGENTA+"1.查看问题详情\n2.提问\n3.添加问题\n4.添加聊天内容\n5.保存学习圈全部问题\n6.删除问题\n7.返回上一级\n8.结束问题\n"+Fore.RED+"请选择需要执行的任务:")
    if int(ques_choice)==1:
        question_detail(question_privatelists)
    elif int(ques_choice)==2:
        question_add()
    elif int(ques_choice)==4:
        question_chatadd(question_privatelists)
    elif int(ques_choice)==5:
        savecount=input("确认要保存学习圈的所有问题吗?[Y/n]")
        if savecount=="y" or savecount=="Y":
            questionsSave()
    elif int(ques_choice)==6:
        delSubmitQuestion(question_privatelists)
    elif int(ques_choice)==8:
        endSubmitQuestion(question_privatelists)

#打印教师信息
def teacherlist():
    questionlist_2=requests.get("https://padapp.msyk.cn/ws/student/homework/studentHomework/searchSubjectInfo?studentId="+studentId+"&unitId="+unitId).text
    #print(questionlist_2)
    studentSubjectList= json.loads(questionlist_2).get('studentSubjectList') 
    for subjectnum in range(len(studentSubjectList)):
        name=studentSubjectList[subjectnum]['name']
        teacherName=studentSubjectList[subjectnum]['teacherName']
        code=studentSubjectList[subjectnum]['code']
        userId=studentSubjectList[subjectnum]['userId']
        print(code,Back.WHITE+Fore.MAGENTA+name,Fore.YELLOW+teacherName,userId)

#打印个人问题列表
def question_privatelist():
    count=1
    question_privatelists=[]
    print(Fore.MAGENTA+"我的问题:")
    question_privatelist_2=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/getSubmitQuestion?userId="+studentId+"&ownerType=1&unitId="+unitId+"&endQuestionType=&subjectCode=&startTime=&endTime=&onlyShowPublic=&pageIndex=1&pageSize=200").text
    data=json.loads(question_privatelist_2).get('data')
    #print(data['submitQuestionList'])
    for my_question_num in range(len(data['submitQuestionList'])):
        redDot=lambda: Fore.RED+" 有老师回复" if int(data['submitQuestionList'][my_question_num]['redDot']) != 0 else ""
        isPublic=lambda: Fore.RED+" 已公开" if int(data['submitQuestionList'][my_question_num]['isPublic']) != 0 else " 未公开"
        chattingRecordsNum=data['submitQuestionList'][my_question_num]['chattingRecordsNum']
        questionDescribe=data['submitQuestionList'][my_question_num]['questionDescribe']
        subjectName=data['submitQuestionList'][my_question_num]['subjectName']
        audioUrlList=data['submitQuestionList'][my_question_num]['audioUrlList']
        picUrlList=data['submitQuestionList'][my_question_num]['picUrlList']
        uuid=data['submitQuestionList'][my_question_num]['uuid']
        print("序号:"+str(count)," ",Back.WHITE+Fore.MAGENTA+subjectName,"  "+Fore.GREEN+uuid+"\n"+Fore.CYAN+"状态  "+"回复数:"+str(chattingRecordsNum)+redDot()+isPublic()+"\n",Fore.YELLOW+questionDescribe)
        question_privatelist_count=[uuid,audioUrlList,picUrlList]
        question_privatelists.append(question_privatelist_count)
        count+=1
    #print(question_privatelists)
    return question_privatelists

#1.查看问题详情
def question_detail(question_privatelists):
    global studentId,unitId
    number=input(Fore.CYAN+"请输入问题uuid或序号:")
    try:
        submitQuestionUuId=question_privatelists[int(number)-1][0]
    except:
        submitQuestionUuId=number
    print("消息:")
    try:
        audioUrlList=question_privatelists[int(number)-1][1]
        picUrlList=question_privatelists[int(number)-1][2]
    except (IndexError, ValueError) as e:
        for question in question_privatelists:
            if question[0]==submitQuestionUuId:
                audioUrlList=question[1]
                picUrlList=question[2]
    if 'audioUrlList' not in locals():
        offer=input("这个问题不是你的问题或已经删除，是否手动提供信息?[Y/n]")
        if offer=='Y' or offer=='y':
            studentId=input("请输入用户ID  ")
            unitId=input("请输入学校ID  ")
        else:
            print("已手动退出")
            return
    try:
      if audioUrlList:
        print("音频列表:")
        for audioUrl in audioUrlList:
            print(Fore.GREEN+audioUrl['url'])
      if picUrlList:
        print("图片列表:")
        for picUrl in picUrlList:
            print(Fore.GREEN+picUrl)
    except:
        pass
    question_detail_2=requests.get("https://learningapp.msyk.cn/ws/chattingRecords/getChattingRecords?submitQuestionUuId="+submitQuestionUuId+"&unitId="+unitId+"&userId="+studentId).text
    data=json.loads(question_detail_2).get('data')
    print("聊天记录:")
    for question_detail_num in range(len(data['chattingRecordsList'])):
        question_detail=data['chattingRecordsList'][question_detail_num]['chatContent']
        picUrlList=data['chattingRecordsList'][question_detail_num]['picUrlList']
        audioUrlList=data['chattingRecordsList'][question_detail_num]['audioUrlList']
        creationTime=data['chattingRecordsList'][question_detail_num]['creationTime']
        creationTime=timestamp_to_date(creationTime)
        realName=data['chattingRecordsList'][question_detail_num]['realName']
        ownerType=data['chattingRecordsList'][question_detail_num]['ownerType']
        if int(ownerType)==1:
            type_text=""
        elif int(ownerType)==2:
            type_text=Fore.RED+"老师"
        print(Fore.YELLOW+realName,type_text,Fore.GREEN+creationTime)
        print(question_detail)
        if audioUrlList:
            print("音频列表:")
            for audioUrl in audioUrlList:
                print(Fore.GREEN+audioUrl['url'])
        if picUrlList:
            print("图片列表:")
            for picUrl in picUrlList:
                print(Fore.GREEN+picUrl)

#2.提问
def question_add():
    if "classId" not in globals():
        print("未检测到classId，退出流程")
        return
    teacherId=input(Fore.CYAN+"请输入要提问教师的ID(选填)  ")
    subjectCode=input(Fore.CYAN+"请输入学科码(不填则为空问题)  ")
    classId=input(Fore.CYAN+"请输入班级ID(选填)  ")
    content=input(Fore.YELLOW+"请输入描述(选填)  ")
    question_privatelist_1=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/addSubmitQuestion?studentId="+studentId+"&content="+content+"&picUrls=[]&aduioList=[]&unitId="+unitId+"&homeworkName=&orderNum=0&teacherId="+teacherId+"&subjectCode="+subjectCode+"&questionId=&classId="+classId)
    question_privatelist_2=question_privatelist_1.json()
    if question_privatelist_2["message"]=="success":
        print("问题创建成功")
    else:
        print(question_privatelist_2)

#4.添加聊天内容
def question_chatadd(question_privatelists):
    qwerid=input(Fore.CYAN+"请输入自己的ID(如留空则默认使用学生ID)")
    if qwerid=="":
        qwerid=studentId
    ownerType=input(Fore.CYAN+"请输入自己的用户类型 1.学生 2.老师")
    submitQuestionUuIds=input(Fore.YELLOW+"请输入问题ID或问题序号")
    if len(submitQuestionUuIds)!=32:
        try:
            submitQuestionUuIds=question_privatelists[int(submitQuestionUuIds)-1][0]
        except:
            print(submitQuestionUuIds)
            print("输入解析失败，请检查输入内容")
            return
    content=input(Fore.GREEN+"请输入描述")
    print("https://learningapp.msyk.cn/ws/chattingRecords/addChattingRecord?userId="+qwerid+"&ownerType="+ownerType+"&content="+content+"&picUrls=%5B%5D&aduioList=%5B%5D&submitQuestionUuIds="+submitQuestionUuIds+"&unitId="+unitId)
    question_chatadd_2=requests.get("https://learningapp.msyk.cn/ws/chattingRecords/addChattingRecord?userId="+qwerid+"&ownerType="+ownerType+"&content="+content+"&picUrls=%5B%5D&aduioList=%5B%5D&submitQuestionUuIds="+submitQuestionUuIds+"&unitId="+unitId).json()
    if question_chatadd_2["message"]=="success":
        print("消息回复成功")
    else:
        print(question_chatadd_2)

#5.保存学习圈全部问题
def questionsSave():
    uuids=[]
    question_privatelist_2=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/getSubmitQuestion?userId="+studentId+"&ownerType=1&unitId="+unitId+"&endQuestionType=&subjectCode=&startTime=&endTime=&onlyShowPublic=&pageIndex=1&pageSize=200").text
    data=json.loads(question_privatelist_2).get('data')
    #print(data)
    for my_question_num in range(len(data['submitQuestionList'])):
        #print(data['submitQuestionList'][my_question_num])
        uuids.append(data['submitQuestionList'][my_question_num]['uuid'])
    print(uuids)
    for submitQuestionUuId in uuids:
        new_folder_name=submitQuestionUuId
        new_folder_path = os.path.join(os.getcwd(), userId,new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        count=1
        coun=1

        question_info=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/getSubmitQuestionInfo?submitQuestionUuId="+submitQuestionUuId+"&unitId="+unitId).text
        data=json.loads(question_info).get('data')
        print(data)
        submitQuestionDto=data['submitQuestionDto']
        picUrlList=submitQuestionDto['picUrlList']
        audioUrlList=submitQuestionDto['audioUrlList']
        questionDescribe=submitQuestionDto['questionDescribe']
        if questionDescribe:
            with open(os.path.join(new_folder_path,"文本.txt"),"a") as file:
                file.write("问题描述:"+questionDescribe+"\n")
        for picUrl in picUrlList:
            file_place=os.path.join(new_folder_path,str(count)+".jpg")
            download(picUrl,new_folder_name+str(count),file_place)
            count+=1
        for audioUrl in audioUrlList:
            file_place=os.path.join(new_folder_path,str(count)+".aac")
            download(audioUrl['url'],new_folder_name+str(coun),file_place)
            coun+=1
        
        question_detail_2=requests.get("https://learningapp.msyk.cn/ws/chattingRecords/getChattingRecords?submitQuestionUuId="+submitQuestionUuId+"&unitId="+unitId+"&userId="+studentId).text
        data=json.loads(question_detail_2).get('data')
        #print(data)
        for content in data['chattingRecordsList']:
            print(content)
            picUrlList=content['picUrlList']
            audioUrlList=content['audioUrlList']
            chatContent=content['chatContent']
            realName=content['realName']
            if chatContent:
                with open(os.path.join(new_folder_path,"文本.txt"),"a") as file:
                    file.write(realName+": "+chatContent+"\n")
            for picUrl in picUrlList:
                file_place=os.path.join(new_folder_path,str(count)+".jpg")
                download(picUrl,new_folder_name+str(count),file_place)
                count+=1
            for audioUrl in audioUrlList:
                file_place=os.path.join(new_folder_path,str(count)+".aac")
                download(audioUrl['url'],new_folder_name+str(coun),file_place)
                coun+=1
#8.结束问题
def endSubmitQuestion(question_privatelists):
    submitQuestionUuIds=input(Fore.YELLOW+"请输入问题ID或问题序号")
    if len(submitQuestionUuIds)!=32:
        try:
            submitQuestionUuIds=question_privatelists[int(submitQuestionUuIds)-1][0]
        except:
            print(submitQuestionUuIds)
            print("输入解析失败，请检查输入内容")
            return
    data=post("https://learningapp.msyk.cn/ws/submitQuestion/endSubmitQuestion",submitQuestionUuIds="['"+submitQuestionUuIds+"']",unitId=unitId).json()
    if data["message"]=="success":
        print("问题结束成功")
    else:
        print(data)

#6.删除问题
def delSubmitQuestion(question_privatelists):
    print(Fore.RED+"注意:你正在删除问题!\n删除后无法恢复数据")
    submitQuestionUuIds=input(Fore.YELLOW+"请输入问题ID或问题序号")
    if len(submitQuestionUuIds)!=32:
        try:
            submitQuestionUuIds=question_privatelists[int(submitQuestionUuIds)-1][0]
        except:
            print(submitQuestionUuIds)
            print("输入解析失败，请检查输入内容")
            return
    choose=input("是否确定删除问题"+submitQuestionUuIds+"?[Y/n]")
    if choose=='Y' or choose=='y':
        data=post("https://learningapp.msyk.cn/ws/submitQuestion/delSubmitQuestion",submitQuestionUuIds="['"+submitQuestionUuIds+"']",unitId=unitId,type=2).json()
        if data["message"]=="success":
            print("问题删除成功")
        else:
            print(data)
    else:
        print(Fore.WHITE+"已取消操作")


##################主菜单部分################
#循环菜单
def menu():
    try:
        getAccountInform()
        homeworklist(studentId,unitId)
    except:
        loginMenu()
    while True:
        do_it=input(Fore.MAGENTA+"1.作业答案获取\n2.查看消息\n3.跑作业id\n4.学习圈(开发中,部分能用)\n5.项目化学习\n6.退出登录\n7.跑作业id(快速)\n"+Fore.RED+"请输入需要执行的任务:")
        if int(do_it)==1:
            get_homework()
        elif int(do_it)==2:
            information_numget()
            informationlist()
        elif int(do_it)==3:
            getUnreleasedHWID()
        elif int(do_it)==4:
            questionmenu()
        elif int(do_it)==5:
            projectmenu() 
        elif int(do_it)==6:
            open("ProfileCache.txt","w",encoding='utf-8').write("")
            print(Fore.CYAN+"已清空 ProfileCache 登录缓存。")
            ProfileImport=input(Fore.CYAN+"请提供登录信息(如无则执行设备信息登录):")
            try:
                setAccountInform(ProfileImport)
            except:
                loginMenu()
                homeworklist(studentId,unitId)
        elif int(do_it)==7:
            try:
                print("可能需要几分钟分析数据，请耐心等待")
                getHomeworkId_new.getHomeworkId(studentId,unitId,classId)
            except Exception as e:
                print(e,"id登录模式下暂不支持快速模式")
        else:
            get_homework()

#程序主体
logo()
menu()









#
