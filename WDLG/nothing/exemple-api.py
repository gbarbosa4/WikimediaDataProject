import wikipedia
import requests
import cairosvg


PAGES = ['2016 Summer Olympics','London']

for page in PAGES:
    wikipage = wikipedia.page(page)
    print ("Page Title: ",wikipage.title)
    print ("Page URL: ",wikipage.url)
    cairosvg.svg2png(url="https://upload.wikimedia.org/wikipedia/en/d/df/2016_Summer_Olympics_logo.svg", write_to="/WikimediaDataLiquidGalaxy/static/images/image2222.png")
    print (" - Main Image: ",wikipage.images)



