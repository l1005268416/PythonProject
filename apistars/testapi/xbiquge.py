import bs4
import pathlib
import requests

class biquge:
    def __init__(self):
        self.allbookurl="http://www.xbiquge.la/xiaoshuodaquan/"
        self.baseurl="http://www.xbiquge.la"
        self.ecoding="utf-8"
        self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                                  "q=0.8,application/signed-exchange;v=b3",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/74.0.3729.131 Safari/537.36",
                        "Accept-Language": "zh-CN,zh;q=0.9"}
    def getallbook(self):
        req=requests.get(self.allbookurl)
        req.encoding=self.ecoding
        soup = bs4.BeautifulSoup(req.text, "lxml")
        libooks=soup.find_all("li")
        books=[]
        for libook in libooks:
            bookhtml=libook.find("a")
            books.append([bookhtml["href"],bookhtml.text])
        return books

    def getmulu(self,url):
        req = requests.get(url)
        req.encoding = self.ecoding
        soup = bs4.BeautifulSoup(req.text,"lxml")
        ddtitles = soup.find_all("dd")
        titles = []
        for ddtitle in ddtitles:
            titlehtml = ddtitle.find("a")
            titles.append([self.baseurl+titlehtml['href'], titlehtml.text])
        return titles

    def gettxt(self,url):
        req=requests.get(url, headers=self.headers)
        req.encoding=req.apparent_encoding
        soup=bs4.BeautifulSoup(req.text,"lxml")

        txt=soup.find(id='content')
        return str(txt).replace('<br/>','\n')

# gtitles = getmulu("http://www.xbiquge.la/10/10489/", "utf-8")
# print(gtitles)

def start():
    bqg = biquge()
    history="history.txt"
    path=pathlib.Path(history)
    if path.exists():
        txtfile=open(history)
        txt=txtfile.read()
    else:
        bookname=input("输入搜索的书籍：")
        bqkallbook = bqg.getallbook()
        findresults=[]
        number=0
        for bqgbook in bqkallbook:
            if bqgbook[1].find(bookname)>=0:
                findresults.append(bqgbook)
                number=number+1
                print("{}.{}".format(number,bqgbook[1]))
        if len(findresults)<1:
            print("没有找到相应书籍。")
            exit()
        bookindex=int(input("请输入书籍序号："))
        print("你选择了《{}》".format(findresults[bookindex-1][1]))
        bookurl = findresults[bookindex-1][0]
        mulu=bqg.getmulu(bookurl)
        number=0
        for title in mulu:
            number=number+1
            print("{}.{}.{}".format(number,title[1],title[0]))
        selecttitle=int(input("请输入要看的章节序号："))
        print("你选择了《{}》".format(mulu[selecttitle - 1][1]))
        print(bqg.gettxt(mulu[selecttitle - 1][0]))

# start()
#bqg = biquge()
#print(bqg.gettxt("http://www.xbiquge.la/10/10489/20604827.html"))
#bqg=biquge()
#bqkallbook=bqg.getallbook()

