# 让天下没有难读的论文（PDFWordTrans辅助英文阅读小工具）
作者：赵亚博

E-Mail: zyabo@foxmail.com 

Blog: [https://www.zhaoyabo.com](https://www.zhaoyabo.com/?p=8695)

Github: https://github.com/zyabo/PDFWordTrans


### 缘起
因为研究方向从**工学**跨到了**医学**，医学英文词汇简直要让我爆了，我还面临着要快速阅读大量文献的需求，所以，我花了半天时间写了这个**辅助英文阅读小工具**，自认为比现有的划译软件更加有助于提升英文专业文献阅读能力，所以分享给大家。



### 初衷
**帮助 科研工作者 快速摆脱 专业英语 困扰**

More big...

Ma体：**让天下没有难读的论文**

More smalllll...
我做了个自觉不错的小工具，不想落灰，希望帮助到大家

### 适合对象
刚入新行业，需要大量阅读英文文献，遇到了大量非原专业的陌生词汇。

### 工具特色
1.有"已知单词"词库，不会翻译"已知单词"词库中的词汇；

2.对非（"已知单词"词库+"已知单词"词库）中的词汇使用百度翻译API进行精准翻译，并存入"已知单词"词库中，随着"已知单词"词库增加，翻译速度会逐步加快；

3.直接将单词翻译标注在单词下，可以逐步适应纯英文阅读。


### 使用步骤
#### 0.准备
申请百度翻译API（标准版，1秒请求一次，永久免费），获取 appid 和 secretKey，并填入py文件中。
不需要升级为收费版本，因为建立了词典后，会在本地记录已经查询的词汇，所以后期基本不用查询，只用本地词典即可，翻译速度也会越来越快。

#### 1.第三方包


pip install selenium

pip install googletrans

pip install google_trans_new

pip install Beautifulsoup4

pip install lxml

pip install PyMuPDF

pip install pdfminer


#### 2.运行程序
python PDFWordTrans.py


文档：我是pdf.pdf

翻译后的文档：@#@\_我是pdf.pdf

### 效果
#### Version 1.0 
![image](https://user-images.githubusercontent.com/8077949/173987805-53efd0e6-7061-427c-91e5-eb738f3a60b0.png)

### History
#### Version 1.0 
##### Time
2022.6.16 
##### New features


### TODO
1. UI.
2. Multilingual support, such as CN2EN.
3. Make the added notes a layer of the pdf.
4. "PDF is evil!" PDF是一种文字排版格式，其元数据中记录的是行信息，非句子或段落信息（与word完全不同），加上期刊论文大部分是双列与单列混合、图文表混合，导致解译pdf时非常困难，我使用了pdfminer第三方包进行解译，仍然存在一些小问题，后续在pdf解译上可以继续做一些工作。

### Join us
我已经修复了里面的许多bug，但是pdf的格式中存在许多很让人无语的问题，肯定还会出现bug，大家如果遇到了，欢迎留言或给我邮件，也希望有大神能一起维护升级这个小工具，**帮助科研工作者快速过了专业英语这一关**。



