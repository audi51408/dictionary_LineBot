from googletrans import Translator
import requests
translator = Translator()
def translate(input, src_lang='eng', to_lang='zh-TW'):
    googleapis_url = 'https://translate.googleapis.com/translate_a/single'
    url = '%s?client=gtx&sl=%s&tl=%s&dt=t&q=%s' % (googleapis_url,src_lang,to_lang,input)
    print(url)
    data = requests.get(url).json()
    print("data:",data)
    print("------------------------")
    res = ''.join([s[0] for s in data[0]])
    return res
def addChineseToEnglish(string,row):
    # print("row:   ",row)
    after_treans = translate(row)
    # print("after_treans",after_treans)
    string += row+"\n"+after_treans+"\n"+"\n"
    # print("string:",string)
    return string
#點擊按鈕后執行的函數
def changeString(content):
    string_input=''
    string = ""
    lastline = ""
    after_treans = ""
    row_list = content.split('\n')
    for i in range(len(row_list)):
        row = row_list[i]
        print("start--------------")
        # print("row:",row)
        if row =="":
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
                lastline+=" "+list[0]+'.'
                string = addChineseToEnglish(string,lastline)
                #中間句子
                for i in range(1,len(list)-1):
                    string = addChineseToEnglish(string,list[i]+".")
                #最後一句
                lastline = list[-1]

        #一行內沒有句號
        elif "." not in row:
            if row!= row_list[-1]:
                lastline += row
                continue
            else:
                # print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
                string = addChineseToEnglish(string,row)
                # print("string:   ",string)
        #尾巴是句號
        else:
            # print("尾巴是斷句----------")
            if lastline != "":
                row = lastline + " " +row+'.'
            string = addChineseToEnglish(string,row)
            # print("lastline重製-----------")
            lastline = ""
        # print("string: ",string)

    return string.rstrip()

if __name__ == "__main__":
    print(changeString("where is the car"))
