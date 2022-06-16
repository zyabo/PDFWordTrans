"""
思路

翻译难的词汇


方法流程
1.排除词典
建立“排除词典”，在词典内的不翻译。
包括：
词典以四级词汇及其变体为准。

2.逐个单词读取文档
读取单词的字符大小，后期标注的大小是这个大小的 0.8倍

3.对非词典内的单词翻译
1)去除单词前后的逗号、分号、括号等符号
2)判断是否是英文单词
3)查询字典

4.将翻译的文字，标注在英文词汇下方

5.*增加尺寸后（PyMuPDF），增加行距（可以使用pdfminer）

6.*将增加的标注做为图层 layer

7.保存的pdf命名为：以前名称+"_日期_YBT.pdf"

"""
# pip3 install pysqlite3
# pip install selenium
# pip install googletrans
# pip install google_trans_new
# pip install Beautifulsoup4
# pip install lxml
# pip install PyMuPDF
# pip install pdf2image
# pip install matplotlib
# pip install pdfminer
import os
import shutil
import time
import fitz                           # import PyMuPDF
from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import PDFPageAggregator
from pathlib import Path  # 导入库

# 2.逐个单词读取文档
# 3.对非词典内的单词翻译
# 4.将翻译的文字，标注在英文词汇下方

def TranslateBaiduJson(TextStr, from_lang, to_lang, appid, secretKey):
    import http.client
    import hashlib
    from urllib import parse
    import random
    import json

    if (from_lang == 'en'):
        from_lang = 'en'
        to_lang = 'zh'
    else:
        from_lang = 'zh'
        to_lang = 'en'
    if len(TextStr) == 0:
        dst = ''
    else:
        httpClient = None
        myurl = '/api/trans/vip/translate'

        salt = random.randint(32768, 65536)
        sign = appid + TextStr + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + \
                parse.quote(TextStr) + '&from=' + from_lang + '&to=' + to_lang + \
                '&salt=' + str(salt) + '&sign=' + sign

        while (1):
            dst = ""
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            html = response.read().decode('utf-8')
            html = json.loads(html)
            # print(html)
            if (len(html) > 2):
                dst = html["trans_result"][0]["dst"]
                # print('百度翻译')
                break
            if (len(html) == 2):
                iio  # 为了制造错误，因为不报错

        # time.sleep(1)
    return dst

def transs(TextStr, from_lang, to_lang, appid, secretKey):
    if len(TextStr) != 0:
        try:
            result = TranslateBaiduJson(TextStr, from_lang, to_lang, appid, secretKey)
        except Exception as e:
            result = '对不起，没有完成翻译！'
    else:
        result = ''
    return result

def read_trans_note(pdf_name, Word_lists, Known_WordLists_EN, Known_WordLists_CN, appid, secretKey):
    # 准备文件
    (path_name, file_name) = os.path.split(pdf_name)
    (file_name_front, suffix) = os.path.splitext(file_name)
    new_pdf = os.path.join(path_name, "@#@_" + file_name_front + suffix)
    # new_pdf = os.path.join(path_name , file_name_front + "_@#@" + suffix)
    shutil.copyfile(pdf_name, new_pdf) # 复制

    # 开始 阅读 翻译
    doc = fitz.open(new_pdf)  # or new: fitz.open(), followed by insertPage()
    #Imports Searchable PDFs and prints x,y coordinates
    fp = open(pdf_name, 'rb')
    manager = PDFResourceManager()
    laparams = LAParams()
    dev = PDFPageAggregator(manager, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, dev)
    pages = PDFPage.get_pages(fp)

    n=-1
    # u1=0
    for page in pages:
        n = n + 1
        # print('--- Processing ---')
        print("\n===============================================  " )
        print("================    第 %d 页    ================  " % (n+1) )
        print("===============================================  " )

        interpreter.process_page(page)
        layout = dev.get_result()
        x, y, text = -1, -1, ''
        for textbox in layout:
            if isinstance(textbox, LTText):
                for line in textbox:
                    isLTChar = True
                    try:
                        for char in line:
                            isLTChar = False
                            break
                    except:
                        break
                    if isLTChar is False:
                        for char in line:
                            # If the char is a line-break or an empty space, the word is complete
                            if isinstance(char, LTAnno) or char.get_text() == ' ':
                                if x != -1:
                                    # print('At %r is text: %s' % ((x, y), text))
                                    if 1:
                                        # 1）删除前后非字母  逗号、分号、括号等符号
                                        while 1:
                                            aa=0
                                            if len(text) > 0:
                                                if text[0]==',' or text[0]=='，' or text[0]==';' or text[0]=='；' or text[0]=='）' or text[0]==')' or text[0]=='.' or text[0]=='。' or text[0]=='-' or (not text[0].isalpha()):
                                                    aa = aa+1
                                                    text = text.replace(text[0], "", 1)
                                            if len(text)>0:
                                                if text[-1]==',' or text[-1]=='，' or text[-1]==';' or text[-1]=='；' or text[-1]=='）' or text[-1]==')' or text[-1]=='.' or text[-1]=='。' or text[-1]=='-' or (not text[-1].isalpha()):
                                                    aa = aa + 1
                                                    text = text.replace(text[-1], "", 1)
                                            if aa==0:
                                                # print('AAAAAAAAAAA')
                                                break
                                        # 1）判断是否应该翻译
                                        # if not text[0].isalpha():
                                        #     continue
                                        # 2）进行翻译
                                        if text.lower() not in Word_lists:

                                            """
                                            """
                                            # 存在
                                            if text.lower() in Known_WordLists_EN:
                                                i0 = Known_WordLists_EN.index(text.lower())
                                                Trans_text = Known_WordLists_CN[i0]
                                                UU=1
                                            else: # 不存在
                                                # 读取 已经存的 字母表
                                                try_n = 0
                                                while 1:
                                                    from_lang = 'en'
                                                    to_lang = 'zh'
                                                    Trans_text = transs(text, from_lang, to_lang, appid,
                                                                                          secretKey)
                                                    time.sleep(1.5)
                                                    if Trans_text == '对不起，没有完成翻译！':
                                                        try_n = try_n + 1
                                                        time.sleep(1)
                                                    else:
                                                        break
                                                    # if try_n>100:
                                                    #     break
                                                print(text+" "+Trans_text)

                                                Known_WordLists_EN.append(text.lower())
                                                Known_WordLists_CN.append(Trans_text)


                                            # print(Trans_text)
                                            # 3）标注
                                            page = doc[n]                         # choose some page
                                            rect = fitz.Rect(x, page.cropbox[3]-y + line.height*0.8, x+100, page.cropbox[3]-y+50)   # rectangle (left, top, right, bottom) in pixels
                                            # Trans_text = text
                                            page.insert_textbox(rect, Trans_text,
                                                                fontsize = 4.0 , # choose fontsize (float) line.height * 0.5
                                                                fontname = "china-s",       # a PDF standard font   Times-Roman  Tahoma  fontname="china-s" or fontname="china-ss"
                                                                fontfile = None,                # could be a file on your system
                                                                align = 0,                      # 0 = left, 1 = center, 2 = right
                                                                color = (100/255, 188/255, 188/255))              # 字体颜色
                                            # u1 = u1+1
                                            # if u1 == 8:
                                            #     uu=8
                                            # print("%d "%(u1))

                                            uu=1

                                x, y, text = -1, -1, ''
                            elif isinstance(char, LTChar):
                                text += char.get_text()
                                if x == -1:
                                    x, y, = char.bbox[0], char.bbox[3]


    file = open('KnownWordLists\Known_WordLists_EN.txt', 'w', encoding='utf-8')
    for i in range(len(Known_WordLists_EN)):
        s = str(Known_WordLists_EN[i]) + '\n'
        file.write(s)
    file.close()

    file = open('KnownWordLists\Known_WordLists_CN.txt', 'w', encoding='utf-8')
    for i in range(len(Known_WordLists_CN)):
        s = str(Known_WordLists_CN[i]) + '\n'
        file.write(s)
    file.close()

    doc.saveIncr()   # update file. Save to new instead by doc.save("new.pdf",...)

def find_all_files(files_path):
    """遍历指定文件夹所有指定类型文件"""
    p = Path(files_path)
    files_names = []  # 存储文件路径名称
    for file in p.rglob('*.pdf'):  # 寻找所有txt文件
        file_str = str(file)

        (path_name, file_name) = os.path.split(file_str)
        (file_name_front, suffix) = os.path.splitext(file_name)
        if len(file_name_front)>4:
            if file_name_front[0:4] != '@#@_':
                files_names.append(file_str)  # 以字符串形式保存
    return files_names

if __name__ == '__main__':
    appid = '20160322000016298'
    secretKey = 'Q6c605JuvTTteOuQJixV'

    Word_lists = []
    with open("EnglishWordlists\Highschool_edited.txt", "r") as f:  # 打开文件
        Wordlists = f.read()  # 读取文件
        # print(Wordlists)
        Word_lists = Wordlists.splitlines()

    Known_WordLists_EN=[]
    try:
        with open("KnownWordLists\Known_WordLists_EN.txt", "r", encoding='UTF-8') as f:  # 打开文件
            Known_WordLists_EN = f.read()  # 读取文件
            Known_WordLists_EN = Known_WordLists_EN.splitlines()
    except:
        print('不存在 Known_WordLists_EN.txt')

    Known_WordLists_CN = []
    try:
        with open("KnownWordLists\Known_WordLists_CN.txt", "r", encoding='UTF-8') as f:  # 打开文件
            Known_WordLists_CN = f.read()  # 读取文件
            Known_WordLists_CN = Known_WordLists_CN.splitlines()
    except:
        print('不存在 Known_WordLists_CN.txt')


    # 获取 文件夹下所有非翻译后的 pdf文件

    files_path = 'D:\\Desktop\\PET'  # 文件夹
    files_names = find_all_files(files_path)  # 获取所有文件路径名称

    for pdf_name in files_names:
        print(pdf_name)
        # pdf_name = 'D:\\Desktop\\PET\\science.1235381.pdf'
        read_trans_note(pdf_name, Word_lists, Known_WordLists_EN, Known_WordLists_CN, appid, secretKey)




"""
from stardict import DictCsv

    csvname = os.path.join(os.path.dirname(__file__), 'ecdict.csv')
    dc = DictCsv(csvname)
    # print(dc.match('kisshere', 10, True))
    dc.commit()


    if Trans_text=='对不起，没有完成翻译！':
        trans_text_Line = dc.query(text).get('translation')
        trans_text_s = trans_text_Line.splitlines()
        trans_text_1 = trans_text_s[0]
        trans_text_1_s = trans_text_1.split(". ")
        if len(trans_text_1_s) == 2:
            trans_text = trans_text_1_s[1]
        else:
            trans_text = trans_text_1_s
        # print(trans_text)

    
if 0:
    trans_tmp = dc.query(text)
    if trans_tmp is not None :
        trans_text_Line = trans_tmp.get('translation')
        trans_text_s = trans_text_Line.splitlines()
        trans_text_1 = trans_text_s[0]
        trans_text_1_s = trans_text_1.split(". ")
        if len(trans_text_1_s) == 2:
            trans_text_1_s = trans_text_1_s[1]
        else:
            trans_text_1_s = trans_text_1_s

        trans_text_1_s = trans_text_1_s.split(";")
        trans_text_1_s = trans_text_1_s[0]
        trans_text_1_s = trans_text_1_s.split("；")
        trans_text_1_s = trans_text_1_s[0]
        trans_text_1_s = trans_text_1_s.split(", ")
        trans_text_1_s = trans_text_1_s[0]
        trans_text_1_s = trans_text_1_s.split("（")
        trans_text_1_s = trans_text_1_s[0]
        trans_text_1_s = trans_text_1_s.split("(")
        trans_text_1_s = trans_text_1_s[0]
        Trans_text = trans_text_1_s
    else:
        Trans_text = ''

else:
    while 1:
        from_lang = 'en'
        to_lang = 'zh'
        appid = '20160322000016298'
        secretKey = 'Q6c605JuvTTteOuQJixV'
        Trans_text = Transs.Transs.Translater(text, from_lang, to_lang, appid,
                                              secretKey)
        time.sleep(1)
        if Trans_text == '对不起，没有完成翻译！':
            time.sleep(0.5)
        else:
            break

"""