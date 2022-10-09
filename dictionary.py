import tkinter as tk  #引入tkinter模块
import pyperclip
from googletrans import Translator
 
# maked by Mountain_Zhou_only
# 设置Google翻译服务地址
translator = Translator()
 
window = tk.Tk()
window.title('逐句翻譯')
window.minsize(500,500)
window.iconphoto(False, tk.PhotoImage(file="C:/Users/audic/Desktop/dictionary/book.png"))
 

def deleteInput(input):
    print("清空")
    input.delete(1.0, tk.END)

def translate(input):
    return translator.translate(input, "zh-TW").text
def addChineseToEnglish(string,row):
    after_treans = translate(row)
    string += row+"\n"+after_treans+"\n"+"\n"
    print("string:",string)
    breaktime = 0
    print("breaktime:",breaktime)
    return string
#点击按钮后执行的函数
def changeString():
    text_output.delete('1.0','end')
    index=1
    string_input=''
    breaktime = 0
    string = ""
    lastline = ""
    after_treans = ""
    #把输入到文本框里面的整段论文拼接起来
    while True:
        print("start--------------")
        print("行數:",index)
        if breaktime>=5:
            print("while中斷--------")
            break
        row = text_input.get(str(index)+'.0',str(index)+'.end')
        print("row:",row)
        if row =="":
            index+=1
            breaktime+=1
            continue
        if ". " in row:
            list = row.split(". ")
            if len(list)==2:
                #加入上一句
                lastline+=" "+list[0]+'.'
                string = addChineseToEnglish(string,lastline)
                lastline = list[1]
            else:
                #加入上一句
                lastline+=" "+list[0]
                string = addChineseToEnglish(string,lastline)
                for i in range(1,len(list)-1):
                    string = addChineseToEnglish(string,list[i])
                lastline = list[-1]

        #一行內沒有句號
        elif "." not in row:
            lastline += row
            index+=1
            continue  
        #尾巴是句號
        else:
            print("尾巴是斷句----------")
            if lastline != "":
                row = lastline + " " +row
            string = addChineseToEnglish(string,row)
            print("lastline重製-----------")
            lastline = ""
        index+=1
        print("string: ",string)
        breaktime = 0

    text_output.insert("insert",string)
    pyperclip.copy(string)


#创建文本输入框和按钮
text_input  = tk.Text(window, width=170, height=25) #100的意思是100个平均字符的宽度，height设置为24行
text_output = tk.Text(window, width=170, height=25)
button = tk.Button(window,text="翻譯並複製",command=changeString,padx=32,pady=4,bd=4)
# button2 = tk.Button(window,text="清空",command=print("清空"),padx=32,pady=4,bd=4)
# button2.place(x= 50 ,y= 658)
 
 
#把Text组件和按钮放在窗口上，然后让窗口打开，並處理在窗口内发生的所有事件；
text_input.pack()
text_output.pack()
button.pack()
window.mainloop()