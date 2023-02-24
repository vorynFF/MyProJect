from lxml import etree
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


content = "List_of_school_districts_in_Alabama"

url = 'https://en.wikipedia.org/wiki/' + content
# 请求头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
# 利用请求地址和请求头部构造请求对象
req = urllib.request.Request(url=url, headers=headers, method='GET')
# 发送请求，获得响应
response = urllib.request.urlopen(req)
# 读取响应，获得文本
text = response.read().decode('utf-8')
#获取页面资源

#构造一个etree对象
tree = etree.HTML(text)
#xpath的表达式，得到想要的数据
#在浏览器的开发者工具中预览节点信息，在Chrome浏览器中可直接选择节点，copy xpath表达式

# 从根节点开始，获取body下面的直属div，返回一个对象列表
# res = tree.xpath('/html/body/div')
# print(res)
#获取根节点下面的,所有的div节点
# res=tree.xpath('/html//div')
#从根节点开始，通过索引的形式，获取
# res = tree.xpath('/ html / body / div[2] / div[1] / div[1]')
#从根节点开始，通过属性名称获取,如果属性名唯一，则中间层可以直接 //表示
#res = tree.xpath('/html//div[@class="index-head"]')
# res = tree.xpath('/html//div[@id="index_header"]')

#不从根节点开始查找
#从任意节点开始查询div，即查询所有的div节点
# res = tree.xpath('//div')    #res = tree.xpath('/html//div')
#查看节点中class名字为index-head的div节点
# res = tree.xpath('//div[@class="index-head"]')
#查询class=col0的div下面的所有li节点
# res=tree.xpath('//div[@class="col0"]//li')
#print(len(res),res)

#取值
#取出所有的div中直属值 （不是div直属的值不取）
# res = tree.xpath('/html//div/text()')   #228个
#取出div中的所有下级的值
#res = tree.xpath('/html//div//text()')    #645个
res = tree.xpath('//div[@class="mw-parser-output"]/table/tbody/tr/td[3]/text()')

#你可以找到相应的节点，然后取值就好

#取属性值
#取出class为col0的div下面的第三个li标签中的a标签直属的href的属性值
# res = tree.xpath('//div[@style="padding:0 0.25em"]//li/a/@title')
print(res)
#标签中的所有href值
# res = tree.xpath('//div[@class="col0"]//li//@href')
# print(len(res), res)

#可以设置多个节点
#得到li标签的对象列表
# li = tree.xpath('//div[@class="col0"]//li')
#具体对象中的值，可以循环取值  ./表示在当前目录下
# res = li[2].xpath('./a/@href')
# print(len(res), res)
sum = 0
for i in res:
    y = i.replace("\n", "")
    print(y)
    z = int(y)
    sum = sum + z
print(sum)