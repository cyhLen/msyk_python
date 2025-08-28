import json
import requests

class getHomeworkId:
    def __init__(self,studentId,unitId,classId):
        subjectInfo=post(searchSubjectInfo_URL,studentId=studentId,unitId=unitId)
        #print(subjectInfo.json())
        studentSubjectList=subjectInfo.json()["studentSubjectList"]
        for studentSubject in studentSubjectList:
            if studentSubject["userId"]:
                #print(studentSubject)
                getHomeworkList1(studentSubject["userId"],unitId,studentSubject["code"],classId)
                getHomeworkList2(studentSubject["userId"],unitId,studentSubject["code"],classId)
                getHomeworkList3(studentSubject["userId"],unitId,studentSubject["code"],classId)
        sorted_dict = dict(sorted(homeworkIdDic.items()))
        for key, value in sorted_dict.items():
            print(key, value)

searchSubjectInfo_URL="https://padapp.msyk.cn/ws/student/homework/studentHomework/searchSubjectInfo"
getHomeworkList1_URL="https://padapp.msyk.cn/ws/teacher/homework/getHomeworkByUserIdAndSubjectCodeAndClassId"
getHomeworkList2_URL="https://padapp.msyk.cn/ws/teacher/homework/list"
homeworkIdDic={}

def post(url, **params):
    try:
        response = requests.post(url, params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(homeworkIdDic)
        print(f"请求错误: {e}")
        print("网络连接失败，请检查代理设置")
        exit(1)

def getHomeworkList1(userId,unitId,subjectCode,classId):
    global homeworkIdDic
    response=post(getHomeworkList1_URL,userId=userId,unitId=unitId,classId=classId,subjectCode=subjectCode,pageSize=9999999,statu=-1,homeworkType=-1,pageIndex=1,searchName="")
    #print(response.json())
    sqHomeworkDtos=response.json()["sqHomeworkDtos"]
    if sqHomeworkDtos:
        for sqHomeworkDto in sqHomeworkDtos:
            homeworkIdDic[sqHomeworkDto['id']]=sqHomeworkDto['homeworkName']


def getHomeworkList2(userId,unitId,subjectCode,classId):
    global homeworkIdDic
    response=post(getHomeworkList2_URL,userId=userId,unitId=unitId,groupId=classId,subjectCode=subjectCode,rows=9999999,homeworkType=-1,pageIndex=1,mark=0,modifyType=0,searchName="")
    #print(response.json())
    homeworkList=response.json()["homeworkList"]
    if homeworkList:
        for homework in homeworkList:
            homeworkIdDic[homework['id']]=homework['homeworkName']

def getHomeworkList3(userId,unitId,subjectCode,classId):
    global homeworkIdDic
    response=post(getHomeworkList2_URL,userId=userId,unitId=unitId,groupId=classId,subjectCode=subjectCode,rows=9999999,homeworkType=-1,pageIndex=1,mark=1,modifyType=0,searchName="")
    #print(response.json())
    homeworkList=response.json()["homeworkList"]
    if homeworkList:
        for homework in homeworkList:
            homeworkIdDic[homework['id']]=homework['homeworkName']


if __name__ == "__main__":
    getHomeworkId(studentId,unitId,classId)
   
