import lxml.etree
import urllib

from wikiapi import WikiApi

title = "2016 Summer Olympics"

params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
tree = lxml.etree.parse(urllib.urlopen(url))
print (tree)
revs = tree.xpath('//rev')

all_result_xml = revs[0].text

wikiapi = WikiApi({ 'locale' : 'en'})
index_i = wikiapi.getIndex_substring("{{Infobox",all_result_xml)
index_f = wikiapi.getIndex_substring("{{"+title,all_result_xml)
print (index_i," ",index_f)
infobox_result = all_result_xml[index_i:index_f]

a = infobox_result.split("| ")
for b in a:
    print (b)
