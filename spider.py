from urllib import request
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Spider():
    url = "https://book.douban.com/top250?icn=index-book250-all"

    root_pattern = '<td valign="top">([\s\S]*?)</td>'

    name_pattern = '<a href=([\s\S]*?) title="([\s\S]*?)"([\s\S]*?)>([\s\S]*?)</a>'

    star_pattern = '<span class="rating_nums">([\s\S]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        books = []
        for html in root_html:
            name = re.search(Spider.name_pattern, html).group(2)
            star = re.findall(Spider.star_pattern, html)[0]
            book = {"name": name, "star": star}
            books.append(book)
        return books

    def __refine(self, books):
        l = lambda book:{'name':book['name'].strip(),"star":book['star']}
        return map(l,books)

    def __sort(self,books):
        books = sorted(books,key=self.__sort_seed,reverse=True)
        return books

    def __sort_seed(self,book):
        r = re.findall('^\d+\.\d+?$',book['star'])
        star = float(r[0])
        star *= 10
        return star

    def __show(self,books):
        for rank in range(0,len(books)):
            print('rank:' + str(rank+1) + ' ' + books[rank]['name'] + ' --- ' + books[rank]['star'])

    def go(self):
        htmls = self.__fetch_content()
        books = self.__analysis(htmls)
        books = list(self.__refine(books)) 
        books = self.__sort(books)
        self.__show(books)


spider = Spider()
spider.go()
