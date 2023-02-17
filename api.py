import random
import re
from threading import Thread
import requests
import lxml
from lxml.html import tostring
from ebooklib import epub
from ebooklib import *



def splitListToFour(list):
    listLen = len(list)
    if (listLen % 4) == 0:
        resList = [list[0:(int(listLen / 4))], list[(int(listLen / 4)):(int(listLen / 4 * 2))], list[(int(listLen / 4 * 2)):(int(listLen / 4 * 3))], list[(int(listLen / 4 * 3)):]]
    else:
        listLen -= listLen % 4
        resList = [list[0:(int(listLen / 4))], list[(int(listLen / 4)):(int(listLen / 4 * 2))], list[(int(listLen / 4 * 2)):(int(listLen / 4 * 3))], list[(int(listLen / 4 * 3)):]]
    return resList

def textToHtml(inputText):
    resTextList = []
    textList = inputText.split('\n')
    for text in textList:
        resTextList.append('<p>' + text + '</p>\n')
    return (''.join(resTextList))

def numToText(num):
    numToTextList = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    if len(str(num)) > 3:
        return "the number is too big"
    if len(str(num)) == 1:
        return numToTextList[num]
    elif len(str(num)) == 2:
        if num == 10:
            return "十"
        if (num % 10) == 0:
            return numToTextList[int((num / 10))] + "十"
        if num < 20:
            return "十" + numToTextList[int((num % 10))]
        return numToTextList[int(((num - (num % 10)) / 10))] + "十" + numToTextList[int((num % 10))]
    elif len(str(num)) == 3:
        if (num % 100) == 0:
            return numToTextList[int((num / 100))] + "百"
        if (num % 100) < 10:
            return numToTextList[int(((num - (num % 100)) / 100))] + "百零" + numToTextList[int((num % 100))]
        if ((num % 100) % 10) == 0:
            return numToTextList[int(((num - (num % 100)) / 100))] + "百" + numToTextList[int(((num % 100) / 10))] + "十"
        return numToTextList[int(((num - (num % 100)) / 100))] + "百" + numToTextList[int((((num - ((num % 100) % 10)) % 100) / 10))] + "十" + numToTextList[int(((num % 100) % 10))]

def getBookInformationAPI1(url, noChapterIndex=False):

    encoding = 'utf-8'
    titleXPath = '//*[@id="bookinfo"]/div[2]/div[1]/h1' + '/text()'
    writerXPath = '//*[@id="bookinfo"]/div[2]/div[1]/span/a' + '/text()'
    introductionXPath = '//*[@id="bookintro"]/p' + '/text()'
    contentMenuXPath = '//*[@id="chapterList"]/li'
    contentNameXPath = 'a/text()'
    contentURLXPath = 'a/@href'
    contentXPath = '//*[@id="TextContent"]'

    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
    headers = {'User-Agent': random.choice(user_agent_list)}

    repr = requests.get(url, headers=headers)
    repr.encoding = encoding
    html = lxml.etree.HTML(repr.content,lxml.etree.HTMLParser(encoding=encoding))
    def getTitle():
        return html.xpath(titleXPath)[0]
    def getWriter():
        return html.xpath(writerXPath)[0]
    def getIntroduction():
        return textToHtml(html.xpath(introductionXPath)[0].replace("　　", "\n"))
    def getContent():
        chapterInformationList = html.xpath(contentMenuXPath)
        chapterContenList = {}
        chapterIndex = 1
        for chapterInformaiton in chapterInformationList:
            # 注意这边是对个别小说的特殊处理，如需打包其他小说，请自行修改
            title = chapterInformaiton.xpath(contentNameXPath)[0]
            if noChapterIndex:
                title = "第" + numToText(chapterIndex) + "章 " + title

            chapterUrl = 'https://www.1718k.com' + chapterInformaiton.xpath(contentURLXPath)[0]
            chapterContentRepr = requests.get(chapterUrl, headers=headers)
            chapterContentHtml = lxml.etree.HTML(chapterContentRepr.content,lxml.etree.HTMLParser(encoding=encoding))
            chapterContent = tostring(chapterContentHtml.xpath(contentXPath)[0], encoding=encoding).decode(encoding)
            chapterContenList[title] = chapterContent
            chapterIndex += 1
        return chapterContenList

    return getTitle(), getWriter(), getIntroduction(), getContent()

def getBookInformationAPI2(url, noChapterIndex=False):

    encoding = 'utf-8'
    titleXPath = '/html/body/section/div/div/header/h1' + '/text()'
    writerXPath = '/html/body/section/div/div/header/h1' + '/text()'
    introductionXPath = '/html/body/section/div/div/article/p[2]' + '/text()'
    contentMenuXPath = '/html/body/section/div/div/article/ul/li'
    contentURLXPath = 'a/@href'
    contentXPath = '//*[@id="text"]'

    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
    headers = {'User-Agent': random.choice(user_agent_list)}

    repr = requests.get(url, headers=headers)
    repr.encoding = encoding
    html = lxml.etree.HTML(repr.content,lxml.etree.HTMLParser(encoding=encoding))

    class GetPageThread(Thread):
        def __init__(self, urlList):
            '''
            :param func: 可调用的对象
            :param args: 可调用对象的参数
            '''
            Thread.__init__(self)
            self.urlList = urlList

        def run(self):
            self.result = self.getPage(self.urlList)

        def getResult(self):
            return self.result

        def getPage(self, urlList):
            pageContent = ''
            for page in urlList:
                pageUrl = page.xpath(contentURLXPath)[0]
                pageResp = requests.get(pageUrl, headers=headers)
                pageResp.encoding = encoding
                pageHtml = lxml.etree.HTML(pageResp.content,lxml.etree.HTMLParser(encoding=encoding))
                pageContent = pageContent + tostring(pageHtml.xpath(contentXPath)[0], encoding=encoding).decode(encoding)
            return pageContent
    def getTitle():
        return html.xpath(titleXPath)[0].split('_')[0]
    def getWriter():
        return html.xpath(writerXPath)[0].split('_')[0]
    def getIntroduction():
        return textToHtml(html.xpath(introductionXPath)[0].split('文案')[1].replace("　　", "\n"))
    def getContent():
        chapterContentDict = {}
        pageInformationList = html.xpath(contentMenuXPath)
        pageContent = ''
        
        splitList = splitListToFour(pageInformationList)
        getPageThreadList = [GetPageThread(splitList[0]), GetPageThread(splitList[1]), GetPageThread(splitList[2]), GetPageThread(splitList[3])]
        getPageThreadList[0].start()
        getPageThreadList[1].start()
        getPageThreadList[2].start()
        getPageThreadList[3].start()
        getPageThreadList[0].join()
        getPageThreadList[1].join()
        getPageThreadList[2].join()
        getPageThreadList[3].join()

        pageContent = getPageThreadList[0].getResult() + getPageThreadList[1].getResult() + getPageThreadList[2].getResult() + getPageThreadList[3].getResult()
        pageContent = pageContent.replace('<p>　　', '').replace('</p>', '').replace('</div><div class="book_con fix" id="text">', '')
        contenPattern = re.compile(r'(?:^|\n)(第.*章.*)')
        contentResult = contenPattern.findall(pageContent)
        print(contentResult)
        chapterIndex = 0
        for chapterTitle in contentResult:
            if (chapterIndex + 1) != len(contentResult):
                chapterContentDict[chapterTitle] = textToHtml(pageContent.split(chapterTitle + '\n')[1].split('\n' + contentResult[chapterIndex + 1])[0])
            else:
                chapterContentDict[chapterTitle] = textToHtml(pageContent.split(chapterTitle + '\n')[1])
            chapterIndex += 1
        return chapterContentDict

    return getTitle(), getWriter(), getIntroduction(), getContent()

def getBookInformationAPI3(url, noChapterIndex=False):

    encoding = 'utf-8'
    titleXPath = '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/h1' + '/text()'
    writerXPath = '/html/body/div[3]/div[1]/div/div/div[2]/div[1]/div/p[1]' + '/text()'
    introductionXPath = '/html/body/div[3]/div[1]/div/div/div[2]/div[2]' + '/text()'
    contentMenuXPath = '/html/body/div[3]/div[2]/div/div/ul/li'
    contentNameXPath = 'a/text()'
    contentURLXPath = 'a/@href'
    contentXPath = '//*[@id="content"]'


    repr = requests.get(url)
    repr.encoding = encoding
    html = lxml.etree.HTML(repr.content,lxml.etree.HTMLParser(encoding=encoding))
    def getTitle():
        return html.xpath(titleXPath)[0]
    def getWriter():
        return html.xpath(writerXPath)[0]
    def getIntroduction():
        return textToHtml(html.xpath(introductionXPath)[0].replace("　　", "\n"))
    def getContent():
        chapterInformationList = html.xpath(contentMenuXPath)
        chapterContenList = {}
        chapterIndex = 1
        print('获取书本章节中\n总章节数:' + str(len(chapterInformationList)) + '\n当前进度:')
        for chapterInformaiton in chapterInformationList:
            print('\r' + '=' * int(((chapterIndex / len(chapterInformationList)) * 100)) + '>' + chapterIndex + '/' + str(len(chapterInformationList)), end='')
            # 注意这边是对个别小说的特殊处理，如需打包其他小说，请自行修改
            title = chapterInformaiton.xpath(contentNameXPath)[0]
            if noChapterIndex:
                title = "第" + numToText(chapterIndex) + "章 " + title

            chapterUrl = url + chapterInformaiton.xpath(contentURLXPath)[0]
            chapterContentRepr = requests.get(chapterUrl)
            chapterContentHtml = lxml.etree.HTML(chapterContentRepr.content,lxml.etree.HTMLParser(encoding=encoding))
            chapterContent = tostring(chapterContentHtml.xpath(contentXPath)[0], encoding=encoding).decode(encoding)
            chapterContenList[title] = chapterContent
            chapterIndex += 1
        print('\n')
        return chapterContenList

    return getTitle(), getWriter(), getIntroduction(), getContent()

def makeEbook(title, writer, introduction, contens):    
    book = epub.EpubBook()
    
    book.set_title(title)
    book.set_language('zh-cn')
    book.add_author(writer)
    
    book.add_metadata(None, 'meta', '', {"content": "cover-image", "name": "cover"})
    book.add_metadata('DC', 'description', introduction)
    
    c1 = epub.EpubHtml(title='简介',
                       file_name='intro.xhtml',
                       lang='zh-cn')
    c1.set_content('<html><body><h1>简介</h1><p></p>{introduction}</body></html>'.replace("{introduction}", introduction))
    
    
    book.add_item(c1)
    
    with open('cover.jpg', 'rb') as coverFile:
        coverConten = coverFile.read()
    cover = epub.EpubItem(uid="cover-image", file_name="images/cover.jpg", media_type="image/jpeg", content=coverConten)
    book.add_item(cover)


    contenItems = []
    index = 0
    for contenTitle in contens:
        contenItem = epub.EpubHtml(title=contenTitle,
                       file_name=str(index) + '.xhtml',
                       lang='zh-cn')
        contenItem.set_content('<html><body><h1>{title}</h1><p></p>{conten}</body></html>'.replace("{title}", contenTitle).replace("{conten}", contens[contenTitle]))
        contenItems.append(contenItem)
        book.add_item(contenItem)
        index += 1
    
    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                        file_name="style/nav.css",
                        media_type="text/css",
                        content=style)
    book.add_item(nav_css)
    
    
    
    book.toc = (epub.Link('intro.xhtml', '简介', 'intro'),
                  (
                   epub.Section('目录'),
                    (contenItems)
                  )
                )

    
    book.spine = ["nav", c1] + contenItems

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())


    epub.write_epub(title + '.epub', book)
