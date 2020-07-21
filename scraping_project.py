from bs4 import BeautifulSoup
import requests
import random

def Find_All(soup,val):
    class_val = soup.find_all(class_=val)
    return class_val

def About_author(url):
    response = requests.get("http://quotes.toscrape.com"+url)
    desc = BeautifulSoup(response.text,"html.parser")
    birthdate = desc.find(class_="author-born-date").get_text()
    birthplace = desc.find(class_="author-born-location").get_text()
    author_desc = desc.find(class_="author-description").get_text()
    d = author_desc[:150]
    return [birthdate,birthplace,d]
    
def make_guess():
    pass

def setup():
    quote_list = Find_All(soup,"text")
    author_list = Find_All(soup,"author")
    rand_num = random.randint(0,len(quote_list))
    span = (author_list[rand_num]).parent
    href = span.find("a")["href"]
    quote = quote_list[rand_num].get_text()
    author = author_list[rand_num].get_text()
    return quote,author,href


page = random.randint(1,10)
response = requests.get("http://quotes.toscrape.com/page/"+str(page))
soup = BeautifulSoup(response.text, "html.parser")
guess = 4
quote,author,href = setup()
while(True):
    print(quote)
    ask = input("Who said the above quote? ")
    if(ask == author):
        a = input("Well done :) !!!...Do you want to play again? (y/n)")
        if a == 'y':
            quote,author,href = setup()
            guess = 4
            continue
        else:
            print("Thank You for playing!!!")
            break
    else:
        guess -= 1
        author_desc = About_author(href)
        if (guess == 3):
            print(f"Hint 1: Author was born on {author_desc[0]} in {author_desc[1]}")
        elif (guess == 2):
            print(f"Hint 2: The first name starts with {author[0]}")
        elif (guess == 1):
            pos = author.rfind(" ")
            print(f"Hint 3: The last name starts with {author[pos+1]}")
        elif (guess == 0):
            fav_author = author_desc[2].replace(author,"*********")
            print(f"Hint 4: Here's a slight description about the author {fav_author}.....")
        else:
            print(f"You have exhausted all your hints... The author is {author}")
            break