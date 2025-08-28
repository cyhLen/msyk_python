import json
import requests


class resubmit:
    def __init__(self,studentId,unitId,homeworkId,serialNumbers,studentAnswers,answers):
        submit_URL="https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives"
        answersList,studentAnswersList=answers.split(";"),studentAnswers.split(";")
        for i in range(len(answersList)):
            if answersList[i]!=studentAnswersList[i]:
                answersList[i]=''.join('1' if char in answersList[i] else '0' for char in "ABCDEFGHIJ")
        answers=";".join(answersList)
        post(submit_URL,serialNumbers=serialNumbers,answers=answers,studentId=studentId,homeworkId=homeworkId,unitId=unitId,modifyNum=0)
        operation_answersubmit(studentId,unitId,answers,serialNumbers,homeworkId)



def post(url, **params):
    try:
        response = requests.post(url, params=params)
        return response
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        print("网络连接失败，请检查代理设置")
        exit(1)

def operation_answersubmit(studentId,unitId,answers,serialNumbers,homeworkId):
    submiturl="https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives?serialNumbers="+serialNumbers+"&answers="+answers+"&studentId="+studentId+"&homeworkId="+homeworkId+"&unitId="+unitId+"&modifyNum=0"
    #print(submiturl)
    a=requests.get(submiturl)
    print("自动提交选择答案中")
    check=answerSubmitCheck(studentId,unitId,homeworkId,answers)
    if check[0]==True:
        print("重提交成功")
    else:
        print("提交失败，请排查问题或联系作者")




#检测提交是否成功
def answerSubmitCheck(studentId,unitId,homeworkId,answers):
    #print(answers)
    print("检测是否提交成功中…")
    homeworkList_msg=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo",homeworkId=homeworkId,studentId=studentId,unitId=unitId,modifyNum=0)
    homeworkCardList=homeworkList_msg.json()['homeworkCardList']
    studentAnswers=""
    for homeworkCard in homeworkCardList:
        questionType=homeworkCard['questionType']
        if questionType==1 or questionType==2:
            studentAnswer=homeworkCard['studentAnswer']
            if studentAnswers=="":
                studentAnswers+=studentAnswer
            else:
                studentAnswers+=";"+studentAnswer
    #print(studentAnswers)
    if answers==studentAnswers:
        return True,studentAnswers
    else:
        return False,studentAnswers

if __name__ == "__main__":
    resubmit(studentId,unitId,homeworkId,serialNumbers,studentAnswers,answers)
