import requests
import os
from colorama import Fore, Style, init,Back
import json
import hashlib
import time
from retrying import retry
import re


init(autoreset=True)
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

#编辑配置文件
def config_mode():
    try:
        with open("config.conf", 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = ["2","2","2"]
    mode1=input("请选择是否需要保存登录信息(即记住登录):[Y/n]")
    if mode1=='Y' or mode1=='y':
        lines[0]="1"
    else:
        lines[0]="2"
    mode2=input("请选择是否需要极速模式:[Y/n]")
    if mode2=='Y' or mode2=='y':
        lines[1]="1"
    else:
        lines[1]="2"
    with open("config.conf", 'w') as file:
        for line in lines:
            file.write(line.strip()+"\n")

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
                file_url=url_deal(resourceUrl_material)
            print(Fore.GREEN+file_url)
            download_choose=input(Fore.BLUE+"是否要下载该文件？[Y/n]")
            if download_choose=='Y' or download_choose=='y':
                download(file_url,analysistList[o]['title'])
                print(Fore.WHITE+"下载成功")
            else:
                print(Fore.WHITE+"已取消下载")
    else:
        print("无文件")


#两个URL处理函数
def url_deal(resourceUrl_material):
    if str(resourceUrl_material).lower().startswith('http'):
        file_url=resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('//'):
        file_url="https://msyk.wpstatic.cn"+resourceUrl_material
    elif str(resourceUrl_material).lower().startswith('/'):
        file_url="https://msyk.wpstatic.cn"+resourceUrl_material
    else:
        file_url="https://msyk.wpstatic.cn/"+resourceUrl_material
    return file_url

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

#十三位时间戳转换
def timestamp_to_date(timestamp): 
    seconds = timestamp // 1000 # 将13位时间戳转换为秒数 
    time_struct = time.gmtime(seconds) # 将秒数转换为struct_time对象 
    date = time.strftime('%Y-%m-%d %H:%M:%S', time_struct) # 将struct_time对象转换为日期格式 
    return date

################登录缓存###############
#来自msykanswer
def getAccountInform():
    ReturnInform=""
    ProfileImport=""
    try:
        for line in open("ProfileCache.txt", "r",encoding='utf-8').readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            ReturnInform = ReturnInform + line
        print("检测到 ProfileCache，尝试缓存登录中。（如失败自动执行登录流程）")
        setAccountInform(ReturnInform)
    except:
        print("未检测到 ProfileCache，执行登录流程。")
        ProfileImport=input(Fore.CYAN+"可提供未缓存的登录信息(失败则自动执行设备信息登录):")
        try:
            setAccountInform(ProfileImport)
        except:
            print(Fore.RED+"错误：登录信息有误或已经失效。")
            print(Fore.WHITE)
            login()

#获取账号信息(来自msykanswer)
def setAccountInform(result):
    #成功登录 获取账号信息
    if json.loads(result).get('code')=="10000":
        save_json(result,json.loads(result).get('InfoMap').get('realName'))
        open("ProfileCache.txt","w",encoding='utf-8').write(result)
        print("ProfileCache 登录缓存已更新。(下一次优先自动读取)")
        global unitId,id,studentId
        unitId=json.loads(result).get('InfoMap').get('unitId')
        id=json.loads(result).get('InfoMap').get('id')
        studentId=id
        
        #sign1=public_key_decrypt(msyk_sign_pubkey,json.loads(result).get('sign')).split(':')

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

#登录
@retry
def login():
    print(Fore.GREEN+"登录流程执行中…")
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
    try:
        if first_line=="1":
            setAccountInform(login_first)
    except:
        pass

def loginMenu():
    loginway=input(Fore.RED+"请选择登录方式:\n"+Fore.MAGENTA+"1.ID登录\n2.账号密码登录\n3.修改配置\n"+Fore.WHITE)
    if loginway=="1":
        global unitId,studentId
        unitId=input(Fore.CYAN+"请输入学校ID")
        studentId=input("请输入用户ID")
    elif loginway=="3":
        config_mode()
        try:
            assign=studentId
        except:
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
        homework_url=resourceList[o]['resourceUrl']
        resTitle=resourceList[o]['resTitle']
        print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+resTitle)
        file_url=url_deal(homework_url)
        print(Fore.GREEN+file_url)
        download_choose=input(Fore.BLUE+"是否要下载文件？[Y/n]")
        if download_choose=='Y' or download_choose=='y':
            download(file_url,resourceList[o]['resTitle'])
            print(Fore.WHITE+"下载文件成功")
        else:
            print(Fore.WHITE+"已取消下载")
    return homework_url

#答题卡类作业获取
def type7(homeworkId):
    read_2=requests.get("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo?homeworkId="+homeworkId+"&studentId="+studentId+"&modifyNum=0&unitId="+unitId).text
    #print(read_2)
    analysistList=json.loads(read_2).get('analysistList') 
    materialRelas=json.loads(read_2).get('materialRelas') 
    homeworkCardList=json.loads(read_2).get('homeworkCardList') 
    #print(analysistList)
    #resourceUrl_material=analysistList[0]['resourceUrl']
    #resourceUrl_answer=materialRelas[0]['resourceUrl']
    #print(resourceUrl_material)
    #print(resourceUrl_answer)
    homeworkName= json.loads(read_2).get('homeworkName') 
    print("作业名称:",Fore.MAGENTA+Back.WHITE+homeworkName)
    operation_answerget(homeworkCardList,homeworkId)
    
    if len(analysistList)!=0:
        for o in range(0,len(analysistList)):
            resourceUrl_material=analysistList[o]['resourceUrl']
            title=analysistList[o]['title']
            print(Fore.YELLOW+"文件名:",Fore.CYAN+Back.WHITE+title)
            
            file_url=url_deal(resourceUrl_material)
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
            
            file_url=url_deal(resourceUrl_answer)
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
    homeworkStatu=json.loads(typeget_2).get('homeworkStatu')  
    typeget=homeworkStatu['homeworkType']
    #print(typeget)
    return typeget

#作业答案部分
def get_homework():
    homeworkId=input(Fore.YELLOW+"请输入作业ID:")
    typeget=homeworktype_get(homeworkId)
    if typeget==5:
        type5(homeworkId)
    elif typeget==7:
        type7(homeworkId)
    else:
        type7(homeworkId)
        #print(typeget)
        #print(Fore.GREEN+"暂不支持，敬请期待")

#选择题答案打印
serialNumbers,answers="",""
question_list = []
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
            answer=answer_encode(answer)
            if serialNumbers=="":
                serialNumbers+=str(serialNumber)
                answers+=answer
            else:
                serialNumbers+=";"+str(serialNumber)
                answers+=";"+answer
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

#选择答案编码(来自msykanswer)
def answer_encode(answer):
    answer_code=""
    if len(answer)==1:
        return answer
    else:
        if "A" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "B" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "C" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "D" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "E" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "F" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "G" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "H" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "I" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "J" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        return answer_code

#选择题答案提交
def operation_answersubmit(answers,serialNumbers,homeworkId):
    submiturl="https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives?serialNumbers="+serialNumbers+"&answers="+answers+"&studentId="+studentId+"&homeworkId="+homeworkId+"&unitId="+unitId+"&modifyNum=0"
    print(submiturl)
    a=requests.get(submiturl)
    print("自动提交选择答案成功")
    #print(a.text)
    #print(serialNumbers,answers)

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
        #dataup={"homeworkId":StartHWID,"modifyNum":0,"userId":id,"unitId":unitId}
        #res=post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus",dataup,3,str(StartHWID)+'0')
        #print(res)
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
    print(Fore.BLACK+Back.WHITE+"新消息:",Fore.BLACK+Back.WHITE+str(data['num']))


#打印消息列表
def informationlist():
    pagenum=1
    while True:
        inflistget_2=requests.get("https://msgapp.msyk.cn/ws/student/information/informationListForStudent?userId="+studentId+"&type=0&pageSize=20&pageIndex="+str(pagenum)+"&startTime=&endTime=&exigencyType=&subjectCodes=&title=&accessory=0").text
        data= json.loads(inflistget_2).get('data') 
        #print(data)
        informationList=data['informationList']
        #print(informationList[0])
        uuid_list=[]
        for inf_order in range(0,len(informationList)):
            i=inf_order+1
            uuid=informationList[inf_order]['uuid']
            globals()[f'global_var_{i}'] = uuid
            uuid_list.append(uuid)
            print(Fore.YELLOW+"序号:",Fore.YELLOW+str(i),Fore.YELLOW+"发送者:",Fore.YELLOW+informationList[inf_order]['sendUserName'],Fore.YELLOW+"标题:",Fore.YELLOW+informationList[inf_order]['title'])
            print(Fore.BLACK+Back.WHITE+informationList[inf_order]['content'])
        print(Fore.GREEN+"当前第",pagenum,Fore.GREEN+"页")
        cho=input(Fore.MAGENTA+"1.上一页\n2.查看详情\n3.下一页\n4.返回上一级\n"+Fore.RED+"请输入需要执行的任务:")
        cho=int(cho)
        if cho==1:
            print("1")
            pagenum-=1
        elif cho==3:
            print("3")
            pagenum+=1
        elif cho==2:
            print("2")
            informationget(uuid_list)
        elif cho==4:
            print("4")
            break
        else:
            print("1")
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
    contentUrl=data['information']['contentUrl']
    contentUrl_list=[]
    contentUrl_dict={}
    contentUrl_dict['title']='title'
    contentUrl_dict['resourceUrl']=contentUrl
    contentUrl_list.append(contentUrl_dict)
    url_deal_and_download(accessoryList)

##################学习圈部分################

#打印教师信息
def questionlist():
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
    print(Fore.MAGENTA+"我的问题:")
    question_privatelist_2=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/getSubmitQuestion?userId="+studentId+"&ownerType=1&unitId="+unitId+"&endQuestionType=&subjectCode=&startTime=&endTime=&onlyShowPublic=&pageIndex=1&pageSize=20").text
    data=json.loads(question_privatelist_2).get('data')
    #print(data['submitQuestionList'])
    for my_question_num in range(len(data['submitQuestionList'])):
        questionDescribe=data['submitQuestionList'][my_question_num]['questionDescribe']
        subjectName=data['submitQuestionList'][my_question_num]['subjectName']
        uuid=data['submitQuestionList'][my_question_num]['uuid']
        print(Back.GREEN+Fore.MAGENTA+subjectName,"  "+uuid+"\n",Fore.BLACK+Back.WHITE+questionDescribe)

#查看详情
def question_detail():
    submitQuestionUuId=input(Fore.CYAN+"请输入问题uuid")
    question_detail_2=requests.get("https://learningapp.msyk.cn/ws/chattingRecords/getChattingRecords?submitQuestionUuId="+submitQuestionUuId+"&unitId="+unitId+"&userId="+studentId).text
    print(question_detail_2)
    data=json.loads(question_detail_2).get('data')
    for question_detail_num in range(len(data['chattingRecordsList'])):
        question_detail=data['chattingRecordsList'][question_detail_num]['chatContent']
        creationTime=data['chattingRecordsList'][question_detail_num]['creationTime']
        creationTime=timestamp_to_date(creationTime)
        realName=data['chattingRecordsList'][question_detail_num]['realName']
        ownerType=data['chattingRecordsList'][question_detail_num]['ownerType']
        if int(ownerType)==1:
            type_text=""
        elif int(ownerType)==2:
            type_text="老师"
        print(realName,type_text,creationTime)
        print(question_detail)

#提问
def question_add():
    teacherId=input(Fore.CYAN+"请输入要提问教师的ID  ")
    subjectCode=input(Fore.CYAN+"请输入学科码  ")
    classId=input(Fore.CYAN+"请输入班级ID  ")
    content=input(Fore.YELLOW+"请输入描述  ")
    question_privatelist_1=requests.get("https://learningapp.msyk.cn/ws/submitQuestion/addSubmitQuestion?studentId="+studentId+"&content="+content+"&picUrls=[]&aduioList=[]&unitId="+unitId+"&homeworkName=&orderNum=0&teacherId="+teacherId+"&subjectCode="+subjectCode+"&questionId=&classId="+classId)
    question_privatelist_2=question_privatelist_1.text
    print(question_privatelist_2)

#聊天记录添加
def question_chatadd():
    qwerid=input(Fore.CYAN+"请输入自己的ID")
    ownerType=input(Fore.CYAN+"请输入自己的用户类型")
    submitQuestionUuIds=input(Fore.YELLOW+"请输入问题ID")
    content=input(Fore.GREEN+"请输入描述")
    question_chatadd_2=requests.get("https://learningapp.msyk.cn/ws/chattingRecords/addChattingRecord?userId="+qwerid+"&ownerType="+ownerType+"&content="+content+"&picUrls=%5B%5D&aduioList=%5B%5D&submitQuestionUuIds="+submitQuestionUuIds+"&unitId="+unitId).text
    print(question_chatadd_2)

#学习圈菜单	
def questionmenu():
    questionlist()
    question_privatelist()
    ques_choice=input(Fore.MAGENTA+"1.查看问题详情\n2.提问\n3.添加问题\n4.添加聊天内容\n5.结束问题\n6.删除问题\n"+Fore.RED+"请选择需要执行的任务:\n")
    if int(ques_choice)==1:
        question_detail()
    elif int(ques_choice)==2:
        question_add()
    elif int(ques_choice)==4:
        question_chatadd()

##################主菜单部分################

#循环菜单
def menu():
    while True:
        do_it=input(Fore.MAGENTA+"1.作业答案获取\n2.查看消息\n3.跑作业id\n4.学习圈(开发中,部分能用)\n5.退出登录\n"+Fore.RED+"请输入需要执行的任务:")
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
            open("ProfileCache.txt","w",encoding='utf-8').write("")
            print(Fore.CYAN+"已清空 ProfileCache 登录缓存。")
            ProfileImport=input(Fore.CYAN+"请提供登录信息(如无则执行设备信息登录):")
            try:
                setAccountInform(ProfileImport)
            except:
                login()
                homeworklist(studentId,unitId)
        else:
            get_homework()

#程序主体
logo()
try:
    with open('config.conf', 'r') as file:
        print("读取config.conf成功")
        print("当前模式:")
        for line in file:
            file.seek(0)
            lines = file.readlines()
            #print(lines)
            num=len(lines)
            for line in range(0,num):
                print(lines[line].strip())
        file.seek(0)
        global first_line
        first_line = file.readline().strip()
    if first_line=="1":
        getAccountInform()
except:
    print(Fore.RED+"错误:配置文件有误或不存在")
    print("检测到你是第一次使用，请先完成模式配置")
    config_mode()
"""
loginway=input(Fore.RED+"请选择登录方式:\n"+Fore.MAGENTA+"1.ID登录\n2.账号密码登录\n3.修改配置\n"+Fore.WHITE)
if loginway=="1":
    global unitId,studentId
    unitId=input(Fore.CYAN+"请输入学校ID")
    studentId=input("请输入用户ID")
elif loginway=="3":
    config_mode()
    try:
        assign=studentId
    except:
        login()
else:
    login()
    """
try:
    if first_line!="1":
        loginMenu()
except:
    loginMenu()
homeworklist(studentId,unitId)
menu()