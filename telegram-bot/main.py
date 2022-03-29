#Стандартные Модули
from asyncio import sleep
import token

# Сторонние модули
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardMarkup,
                             InlineKeyboardButton, Message)

# Локальные Модули
import anime_handler
import bot_token
import welcome_handler as w_handler

# Bot Initialization
bot = TeleBot(bot_token.token)

# Variables
bot.w_file = "animation"
bot.file_path = "static/happy-anime.mp4"
bot.curr_page = 1




@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:

    if bot.w_file != "text": 
        with open(bot.file_path, "rb") as file:
            if bot.w_file == "photo":
                bot.send_photo(message.chat.id, file)
            elif bot.w_file == "sticker" or bot.w_file == "animated":
                bot.send_sticker(message.chat.id, file)
            elif bot.w_file == "animation":
                bot.send_animation(message.chat.id, file)

    msg_text = w_handler.prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:

    msg_text = w_handler.prep_cmd_msg(message)

    bot.send_message(message.chat.id, msg_text)



@bot.message_handler(commands=["config"])
def config(message: Message) -> None:

    config_keyboard = InlineKeyboardMarkup(row_width=2)

    photo_key = InlineKeyboardButton(text="Photo + Text",
                                     callback_data="photo")
    animation_key = InlineKeyboardButton(text="Animation + Text",
                                     callback_data="animation")
    sticker_key = InlineKeyboardButton(text="Sticker + Text",
                                     callback_data="sticker")
    text_key = InlineKeyboardButton(text="Only text",
                                     callback_data="text")

    config_keyboard.add(photo_key, animation_key, sticker_key, text_key)

    bot.send_message(message.chat.id, " {0.first_name} Select greeting type!".format(message.from_user),
                    reply_markup=config_keyboard)


def _sticker_type(message: Message) -> None:

    sticker_keyboard = InlineKeyboardMarkup(row_width=2)

    standard_key = InlineKeyboardButton(text = "Simple sticker",
                                        callback_data="standard")

    anim_key = InlineKeyboardButton(text = "animated sticker", 
                                    callback_data="animated")


    sticker_keyboard.add(standard_key, anim_key)

    bot.send_message(message.chat.id, "Choose sticker type!",
                        reply_markup=sticker_keyboard)

def _ask_change_text(message: Message) -> None:

    ask_keyboard = InlineKeyboardMarkup(row_width=2)

    yes_key = InlineKeyboardButton(text="Yes",
                                    callback_data="yes")

    no_key = InlineKeyboardButton(text = "No",
                                    callback_data="no")

    ask_keyboard.add(yes_key, no_key)

    bot.send_message(message.chat.id, "Do you want to change a text?",
                     reply_markup=ask_keyboard)



@bot.message_handler(["animesearch"])
def animesearch(message: Message)-> None:

    _ask_anime_title(message, _select_anime_title,
                         _show_search_results)



def _show_search_results(message: Message, search_results: list) -> None:

    bot.send_message(message.chat.id, "Processing your search...")

    msg_text = ""

    for anime in search_results:
        msg_text += f"<a href=\"{anime[1]}\">{anime[0]}</a>\n"

    bot.send_message(message.chat.id, msg_text, parse_mode="html")


@bot.message_handler(commands=["animetop"])


def show_anime_top(message: Message) -> None:

    bot.send_message(message.chat.id, "Top 100 Anime!")

    bot.rankings = anime_handler.ranking()
    page_keyboard = _page_keyboard_init()

    msg_text = ""

    for index in range(10): 
        msg_text += f"{index + 1}, {bot.rankings[index]}\n"

    bot.send_message(message.chat.id, msg_text,
                     reply_markup=page_keyboard)


def _page_keyboard_init() -> InlineKeyboardMarkup:

    page_keyboard = InlineKeyboardMarkup(row_width=4)

    first_key = InlineKeyboardButton(text = "First one",
                                     callback_data="first")

    previous_key = InlineKeyboardButton(text = "<<",
                                        callback_data="previous")

    next_key = InlineKeyboardButton(text = ">>",
                                    callback_data="next")

    last_key = InlineKeyboardButton(text = "Last one",
                                    callback_data="last")

    page_keyboard.add(first_key, previous_key, next_key, last_key)

    return page_keyboard


def _change_page(message: Message) -> None:
    
    page_keyboard = _page_keyboard_init()
    
    msg_text = ""
    
    if bot.curr_page < 1:
        bot.curr_page = 1
    elif bot.curr_page > 10:
        bot.curr_page = 10
    
    for index in range((bot.curr_page - 1) * 10, bot.curr_page * 10):
        msg_text += f"{index + 1}. {bot.rankings[index]}\n"
        
    
    bot.send_message(message.chat.id, msg_text,
                     reply_markup=page_keyboard)

@bot.message_handler(commands=["animeost"])
def animeost(message: Message) -> None:

    _ask_anime_title(message, _select_anime_title, _show_anime_osts)


def _show_anime_osts(message: Message, anime_info: list) -> None:

    index = int(message.text)

    bot.send_message(message.chat.id, 
                        f"Anime Search results:{anime_info[index - 1][0]}")

    songs = anime_handler.osts(anime_info[index - 1][1])

    msg_text = ""

    for song in songs:
        msg_text += song

    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(["animecharacters"])
def animecharacters(message: Message) -> None:
    
    _ask_anime_title(message, _select_anime_title, _show_anime_cast)



def _show_anime_cast(message: Message, anime_info: list) -> None:

    index = int(message.text)

    bot.send_message(message.chat.id, 
                        f"Anime Search results:{anime_info[index - 1][0]}")

    characters = anime_handler.find_characters(anime_info[index - 1][1])

    msg_text = ""

    for i in range(len(characters)):
        msg_text += f"{i + 1}. <a href=\"{characters[i][1]}\">{characters[i][0]}</a>\n"

    bot.send_message(message.chat.id, msg_text, parse_mode="html")


@bot.message_handler(["animesummary"])
def animesummary(message: Message) -> None:

    _ask_anime_title(message, _select_anime_title, _show_anime_summary)



def _show_anime_summary(message: Message, anime_info: list) -> None:
    
    index = int(message.text)

    msg_text = anime_handler.find_summary(anime_info[index - 1][1])

    bot.send_message(message.chat.id, f"Synopsis {anime_info[index - 1][0]}:")
    bot.send_message(message.chat.id, msg_text)



@bot.message_handler(["animetrailer"])
def animetrailer(message: Message) -> None:
    
    _ask_anime_title(message, _select_anime_title, _show_anime_trailer)




def _show_anime_trailer(message: Message, anime_info: list) -> None:
    
    index = int(message.text)

    link = anime_handler.find_trailer(anime_info[index - 1][1])

    bot.send_message(message.chat.id, f"Trailer {anime_info[index - 1][0]}:")
    bot.send_message(message.chat.id, link,
                         disable_web_page_preview=False)



def _ask_anime_title(message: Message, func1, func2) -> None:
    bot.send_message(message.chat.id,
                        "Write the name of the anime(In English)")

    bot.register_next_step_handler(message, func1, func2)

def _select_anime_title(message: Message, func) -> None:
    
    search_results = anime_handler.search(message.text)
    
    msg_text = ""
    
    for index in range(len(search_results)):
        msg_text += f"{index + 1}. <a href=\"{search_results[index][1]}\">{search_results[index][0]}</a>\n"
    
    bot.send_message(message.chat.id, msg_text,
                     parse_mode="html")
    bot.send_message(message.chat.id, 
                     f"Choose Anime: 1 - {len(search_results)}")
    bot.register_next_step_handler(message, func, search_results) 


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call: CallbackQuery) -> None:

    bot.answer_callback_query(call.id)

    _check_file_type(call)

    _check_sticker_type(call)

    _check_text_change(call)

    _check_page_number(call)


def _check_file_type(call):
    if call.data == "photo":
        bot.w_file = "photo"
        bot.file_path = "static/stick.webp"
        bot.send_message(call.message.chat.id, "Send me a photo in .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)
        
    if call.data == "animation":
        bot.w_file = "animation"
        bot.file_path = "static/happy-anime.mp4"
        bot.send_message(call.message.chat.id, "Send me a animation in .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)

    if call.data == "sticker":
        _sticker_type(call.message)


    if call.data == "text":
        bot.w_file = "text"
        bot.send_message(call.message.chat.id, "Send me a Text!")
        bot.register_next_step_handler(call.message, 
                                    w_handler.g_change_text, bot)


def _check_sticker_type(call):
    if call.data == "standard":
        bot.w_file = "sticker"
        bot.file_path = "static/for.webp"
        bot.send_message(call.message.chat.id, "Send me a sticker in .WEBP!")
        bot.register_next_step_handler(call.message, _change_file, call.data)
        
    if call.data == "animated":
        bot.w_file = "animated"
        bot.file_path = "static/sticker.webp"
        bot.send_message(call.message.chat.id, "Send me a sticker in .TGS!")
        bot.register_next_step_handler(call.message, _change_file, call.data)


def _check_text_change(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id,
                            "Send me a Text!")
        bot.register_next_step_handler(call.message,
                                         w_handler.g_change_text, bot)
    
    if call.data == "no":
        bot.send_message(call.message.chat.id,
                                 "Sure Thing!")
        _send_anim(call)


def _send_anim(call: CallbackQuery) -> None:
    with open("static/anim.webp", "rb") as sticker:
        bot.send_sticker(call.message.chat.id, sticker)


def _change_file(message: Message, call_data: str) -> None:

    w_handler.write_file(bot, message, call_data,
                         bot.file_path, bot_token.token)
    
    _ask_change_text(message)


def _check_page_number(call):
    if call.data == "first":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.curr_page = 1
        _change_page(call.message)
    if call.data == "previous":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.curr_page -= 1
        _change_page(call.message)
    if call.data == "next":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.curr_page += 1
        _change_page(call.message)
    if call.data == "last":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.curr_page = 10
        _change_page(call.message)

bot.polling(none_stop=True, interval=0)