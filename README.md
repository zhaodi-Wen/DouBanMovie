# 用BeautifulSoup爬取豆瓣的电影排行榜，并用xlwt把数据保存成excel
**大家好，这是我的第一篇博文，如有不当之处请各位谅解并及时指出！**
**python强大的第三方module，使他成为网络爬虫和各种数据分析的首选工具.**

## 工具
安装了pev的eclipse(具体的安装pev和使用方式请百度或者Google)，如果你习惯用sublime text，可以使用sublime编辑，然后在eclipse上编译运行

## 步骤

1.爬取网页[豆瓣高分电影榜](https://www.douban.com/doulist/240962/?start=0&sort=seq&sub_type=)的内容

根据网页上的信息

![image](http://img.blog.csdn.net/20170819181832238?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

我们建立一个DouBanItem的类，把要爬取的项目列出来，这里我是这样设置的

```
class DouBanItem(object):
"""docstring for DouBanItem"""
    name = None
    point = None
    director = None
    staring = None
    type = None
    country = None
    year = None
```
相信用过scrapy框架的应该有点熟悉这种方式。

2.然后再建立一个GetDouBanMovie类，这里面是整个project的核心，包括url的构造，response的获取，以及内容的抓取，这里我还设置了一个下载函数，用于生成.txt文件。
所以我设置的函数有以下几个
```
def __init__(self)
def getUrls(self)
def getResponseContent(self,url)
def spider(self,urls)
def piplines(self,items)
```

def getUrls(self)函数里面

![image](http://img.blog.csdn.net/20170819215531577?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![image](http://img.blog.csdn.net/20170819215605590?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

我截取前两页的url，可以看出第一张和第二张的区别在于'start='后面的数字，说明每个url的间隔是一个step = 25


![image](http://img.blog.csdn.net/20170819215936612?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

而这里总共有12页，所以问题就很简单了，构造一个urls = []，里面有12个url。
具体的源码我会上传到github，大家可以自行下载参考。


不过在spider函数里我遇到一个问题，想在这里和大家分享一下：
在[](view-source:https://www.douban.com/doulist/240962/?start=0&sort=seq&sub_type=)(其中一个url的源代码)中,我要获取的item中包括这几个
```
导演: 弗兰克·德拉邦特

主演: 蒂姆·罗宾斯 / 摩根·弗里曼 / 鲍勃·冈顿
  
类型: 犯罪 / 剧情
 
制片国家/地区: 美国
 
年份: 1994
```

但是用以下代码
```
content = tag.find('div',attrs={'class':"abstract"})
details = content.get_text()
```
执行后的details结果为
 
``` 
'导演: 弗兰克·德拉邦特        
 主演:让·雷诺/娜塔莉·波特曼/加里·奥德曼     
 类型: 剧情/动作/犯罪        
 制片国家/地区: 法国     
 年份: 1994'
```

它是一个字符串。**（注意这里每个冒号后面都有一个空格，这让我很头疼）**



而我需要获取的只是每个冒号后面的内容。
所以我加了以下的代码

```
details = details.replace(' ','').split()
```

第一次replace后details还是一个字符串，只不过冒号后面的空格不见了
结果如下：

```
'导演:弗兰克·德拉邦特      
 主演:让·雷诺/娜塔莉·波特曼/加里·奥德曼      
 类型: 剧情/动作/犯罪        
 制片国家/地区:法国      
 年份:1994'
```

第二次使用split()后，details就变成了一个list，即

```
['导演:弗兰克·德拉邦特',
'主演:让·雷诺/娜塔莉·波特曼/加里·奥德曼',
'类型:剧情/动作/犯罪',
'制片国家/地区:法国',
'年份:1994']
```

接下来就好办了，分别使用五个split(':')[1]，把冒号后面的内容提取到相应的item上
```python
item.director = details[0].split(':')[1]
item.staring = details[1].split(':')[1]
item.type = details[2].split(':')[1]
item.country = details[3].split(':')[1]
item.year = details[4].split(':')[1]
```
3.使用xlwt把数据保存成一个excel文件所以我又建立了一个saveExcel3.py文件，里面是xlwt的一些基本用法，语法不是很难，只要大家不要把坐标和相应的内容填错就没什么问题。具体的我就不再赘述，大家可以参考我的源码。

4.同时里面有一个log.py文件，他是用于记录运行过程中的各种信息，以便我们知道爬取数据和保存数据成功或者失败的信息，它适用于其他project，大家可以灵活使用。

5.最后整个project的整体框架和运行结果如下如下：

----------------------------------
**这是eclipse的框架图，没有把excel文件显示出来，我也不知道为什么...**

![](http://img.blog.csdn.net/20170819225231033?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

------------------------------------
**这是在sublime text3上的框架图，(sublime 是我最喜欢的编辑器，没有之一)**

![image](http://img.blog.csdn.net/20170819225251847?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

-----------------------------------

**这是在文件里面的框架，这里显示的比较全面**

![image](http://img.blog.csdn.net/20170819225317104?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

------------------------------------
**这是在sublime显示的txt文件部分数据，贴出来只是因为它比较好看**

![image](http://img.blog.csdn.net/20170819225329987?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


----------------------------
**这是部分表格的数据**

![image](http://img.blog.csdn.net/20170819225345874?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvWmhhb2RpX1dlbg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



**最后这是我的第一篇博文，如有缺漏或者错误之处，还请各位海涵，并帮我指出错误。谢谢！！！**


