from googletrans import Translator
import requests

translator = Translator()
def translate(text, src_lang='jap', to_lang='zh-TW'):
    print(type(text))
    googleapis_url = 'https://translate.googleapis.com/translate_a/single'
    url = '%s?client=gtx&sl=%s&tl=%s&dt=t&q=%s' % (googleapis_url,src_lang,to_lang,text)
    print(url)
    data = requests.get(url).json()
    print("data:",data)
    print("------------------------")
    res = ''.join([s[0] for s in data[0]])
    return res
def addChineseToEnglish(string,row):
    after_treans = translate(row)
    string += row+"\n"+after_treans+"\n"+"\n"
    # print("string:",string)
    return string
#點擊按鈕后執行的函數
def changeString(content):
    string_input=''
    string = ""
    lastline = ""
    after_treans = ""
    print("content:",content)
    row_list = content.split('\n')
    for row in row_list:
        print("start--------------")
        # print("row:",row)
        if row =="":
            continue
        string = addChineseToEnglish(string,row)

    return string
if __name__ == "__main__":
    print(changeString(text="焼いよ茹でてよしのトウモロコシアツアツのでのの美味しさっさったらたらたら，，歯ににトウモロコシトウモロコシの皮皮がはさまっさまっもも餘裕餘裕"))
