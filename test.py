from html.parser import HTMLParser
import urllib
import urllib.request
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)
def download_page(url):
    headers = {'Cookie': 'YF-Page-G0=70942dbd611eb265972add7bc1c85888; SUB=_2AkMtkCK-f8NxqwJRmP4WzmLrbYpwwwHEieKbzNNlJRMxHRl-yT9kqmsutRB6BhAMUWJzsjwZtg9fQ7GbkY-HHWbIhcSe; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W504j2F1PMnduYfKznGuSSj; YF-V5-G0=8d795ebe002ad1309b7c59a48532ef7d; _s_tentry=passport.weibo.com; Apache=5253165177621.424.1523363211269; SINAGLOBAL=5253165177621.424.1523363211269; ULV=1523363211282:1:1:1:5253165177621.424.1523363211269:; WBStorage=65eb7e5340cb4756|undefined'}
    request = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(request)
    data = str(response.read(),'utf-8')
    return data

url = 'https://weibo.com/ttarticle/p/show?id=2309404226961558922971'
hp = MyHTMLParser()
html_code = download_page(url)
print(html_code)

# hp.close()
# print(hp.links)

