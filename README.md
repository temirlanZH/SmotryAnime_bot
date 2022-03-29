# SmotryAnime_bot
This bot is almost the same as the previous one except that code became more compact and some functionalities are missing. I turned those functionalities into homework for my students. All the description is copy pasted from previous repository.

Not that simple telegram bot written in Python that gathers info about anime rankings and requested anime info.

# Table of Contents
Project info
Technologies
Features
Available commands Setup

# Project info
This project is built using Python 3.9.7. The main framework used was pyTelegramBotAPI as well as BeautifulSoup4 for some web scraping functions. This project's purpose is to teach my students(at the academy that I work at) Python and how to create a Telegram bot using it. All information related to anime is gathered from MyAnimeList

# Technologies
### Python 3.10.4
### pyTelegramBotAPI 4.3.1
### BeautifulSoup4 4.10.0
# Features
### .PNG, .GIF, .WEBP, .TGS support
Welcome message customization
Top 100 Anime by categories
Anime OST, Synopsis, Trailer, Cast info
# Available commands
## COMMANDS                 DESCRIPTION
### /start                              Starts the bot. Sends the welcome message
### /help                              Shows the list of commands and their description
### /welcomeconfig            Lets user change welcome message type and text message: Photo + text, Sticker + text, Animiation + text, Only text
### /animetop                     Top 100 Anime by categories: Alltime, Airing, Upcoming, Popular, Favourite
### /animesearch                Searches by anime title and sends a message with links
### /animeost                      Searches by anime title and presents a list of anime OSTs
### /animecast                    Searches by anime title and presents a list of anime characters and links to their pages
### /animesummary           Searches by anime title and presents the anime synopsis
### /animetrailer                 Searches by anime title and presents a link to the video

# Setup
Clone this repo to your desired location and use pip install -r requirements.txt to install all of the dependencies.
Once the dependencies are installed you can run the bot in terminal using python main.py.

But before that you should call @BotFather in Telegram and create new bot so that you get the bot token. Once you receive the token place it on the 21st line in main.py instead of the bot_token.token variable.
Your token line should look like this:
bot = TeleBot('your bot token')
