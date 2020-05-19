from bs4 import BeautifulSoup

soup = BeautifulSoup(open('web/game.html'),'html.parser')
print(soup.body.contents[0])
