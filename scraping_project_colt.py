import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader


base_url = "http://quotes.toscrape.com"

def read_quotes(filename):
    with open(filename,"r",encoding="utf8") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)
        

def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote... ")
    print(quote["text"])
    guess = ''    
    while guess.lower() != quote["author"].lower():
        guess = input(f"Who said this? Guesses remaing: {remaining_guesses} ")
        if guess.lower() == quote['author'].lower():
            print("YOU GOT IT RIGHT")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{base_url}{quote['bio-link']}")
            soup = BeautifulSoup(res.text,"html.parser")
            birthdate = soup.find(class_="author-born-date").get_text()
            birthday = soup.find(class_="author-born-location").get_text()
            print(f"Here's a hint: The author was born on {birthdate} {birthday}")
        elif remaining_guesses == 2:
            print(f"Here's a hint: The author's first name starts with {quote['author'][0]}")
        elif remaining_guesses == 1:
            last_initial = quote['author'].split(" ")[1][0]
            print(f"Here's a hint: The author's last name starts with {last_initial}")
        else:
            print(f"Sorry you ran out of guesses. The answer is {quote['author']}")
            break

    again = ''
    while not again.lower() in ('yes','y','n','no'):
        again = input("Would you like to play again? (y/n)")
    if again.lower() in ('yes','y'):
        return start_game(quotes)
    else:
        print("Ok!GoodBye...")

quotes = read_quotes("quotes.csv")
start_game(quotes)