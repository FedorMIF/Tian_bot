import os
import telebot
from telebot import TeleBot, types
import keyboa
from keyboa import keyboa_maker
import bd

bot = TeleBot('1661866696:AAFi8P_OLIstQ2RGmoZFBkXVSZivYMoJIzk')

yn_but = [ 'Да','Нет']

keyboard_menu = types.ReplyKeyboardMarkup(row_width = 2).add( 'Изменить свое имя', 'Добавить напоминание',  'Пока ничего')
keyboard_yn = types.ReplyKeyboardMarkup(row_width = 2).add( 'Да', 'Нет' )

list_commands = ['/help: Список всех комманд;', '/menu: Меню с функциями;', 'Напиши привет, для того что бы познакомиться;']

#keyboard_yn = keyboa_maker(items = yn_but, copy_text_to_callback=True, items_in_row = 2)

what_yn_com = 0

bro = [445894340, 339512152]

def printlist(list_commands):
    l = len(list_commands)
    i = 0
    string = ''
    while i < l:
        string += list_commands[i] + '\n'
        i += 1
    return string

@bot.message_handler(commands=['start'])

def start(mess):
    bd.add_new_user(mess.from_user.id, mess.from_user.first_name)
    bd.give_user_name(mess.from_user.id)
    bot.reply_to(mess, f'Привет, {bd.give_user_name(mess.from_user.id)}, я твой помощник в делах насущных, напиши /help для того что бы увдеть все комманды')

@bot.message_handler(commands=['help'])

def help(mess):
    bot.reply_to(mess, printlist(list_commands))

@bot.message_handler(commands=['menu'])

def get_menu(mess):
    bot.reply_to(mess, 'Выбери что ты хочешь', reply_markup = keyboard_menu )

@bot.message_handler(content_types=['text'])

def com_text(mess):
    if 'привет' in mess.text.lower():
        name = bd.give_user_name(mess.from_user.id)
        bot.send_message(mess.from_user.id, f'Привет, {name}!')
        if mess.from_user.id in bro:
            bot.send_message(mess.from_user.id, f'Салам, братьям админа')

        #else: 
            #bot.send_message(mess.from_user.id, 'Привет, ' + name)

    elif mess.text.lower() == 'изменить свое имя':
        bot.send_message(mess.from_user.id, 'Напиши все новое имя')
        bot.register_next_step_handler(mess, get_name)

    elif mess.text.lower() == 'пока ничего':
        bot.send_message(mess.from_user.id, 'Напши как что-то захочешь /menu')

    elif mess.text.lower() == 'добавить напоминание':
        if bd.create_new_bdrasp(mess.from_user.id): 
            bot.send_message(mess.from_user.id,  'Напиши что тебе напомнить')

        else:
            bot.send_message(mess.from_user.id,  'У тебя уже есть несколько напоминаний, хочешь добавить еще одно?', reply_markup = keyboard_yn)
            global what_yn_com
            what_yn_com = 1
    
    elif mess.text.lower() == 'да':
        if what_yn_com == 0:
            err('wtf', mess)

        elif what_yn_com == 1:
            what_yn_com = 0
            bot.send_message(mess.from_user.id,  'Ага, уже, что тебе еще сделать?', reply_markup = keyboard_menu)

        elif what_yn_com == 2:
            what_yn_com = 0
            msg = bot.send_message(mess.from_user.id, 'Напиши все новое имя')
            bot.register_next_step_handler(msg, ch_name1)
        
        elif what_yn_com == 3:
            what_yn_com = 0
            bot.send_message(mess.from_user.id, 'Хорошо) Тогда я тебя запомню)', reply_markup = keyboard_menu)

    elif mess.text.lower() == 'нет':
        if what_yn_com == 0:
            err('wtf', mess)

        elif what_yn_com == 1:
            what_yn_com = 0
            bot.send_message(mess.from_user.id,  'Ну и иди от сюда', reply_markup = keyboard_menu)

        elif what_yn_com == 2:
            what_yn_com = 0
            bot.send_message(mess.from_user.id,  'Тогда я тебя запомню таким', reply_markup = keyboard_menu)
        
        elif what_yn_com == 3:
            what_yn_com = 0
            bot.send_message(mess.from_user.id,  'Как тебя зовут?')
            bot.register_next_step_handler(mess, get_name)

    else:
        err('wtf', mess)


####################

def add_notification(id, mess):
    bd.add_new_rasp(id, mess)

def get_name(mess):
    ch = bd.add_new_user(mess.from_user.id, mess.text)
    
    if ch == 'T':
        name = bd.give_user_name(mess.from_user.id)
        if name != False: 
            bot.send_message(mess.from_user.id, 'Привет, ' + name + '. Напиши "/menu", что бы ознакомиться с тем, что я могу для тебя сделать')
        
        else:
            err('name_err', mess)
    
    elif ch == "double":
            name = bd.give_user_name(mess.from_user.id)
            if name != False: 
                bot.send_message(mess.from_user.id, f'У меня уже есть твое имя, {name}, хочешь выбрать другое?', reply_markup = keyboard_yn)
                global what_yn_com
                what_yn_com = 2
            else:
                err('name_err', mess)
    
    else: 
        err('err', mess)

def ch_name1(mess):
    ch = bd.edit_user_name(mess.from_user.id, mess.text)
    if ch:
        name = bd.give_user_name(mess.from_user.id)    
        bot.send_message(mess.from_user.id, 'Привет, ' + name + '. Напиши "/menu", что бы ознакомиться с тем, что я могу для тебя сделать')
        
    else:
        err('err', mess)

def err(v, mess):
    if v == 'err':
        bot.send_message(mess.from_user.id, 'Что то пошло не так, попробуй заново')

    elif v == 'name_err':
        bot.send_message(mess.from_user.id, 'Не могу получить твое имя, попробуй заново')

    elif v == 'wtf':
        bot.send_message(mess.from_user.id, 'Я тебя не понимаю( Напиши /help')

#@bot.callback_query_handler(func=lambda call: True)
#def callback_inline(call):
    #global what_yn_com

    #if call.data == 'Да':
        #if what_yn_com == 1:
            #bot.send_message(call.message.chat.id,  'Ага, уже, что тебе еще сделать?')
            #what_yn_com == 0

        #elif what_yn_com == 2:
            #bot.send_message(call.message.chat.id, 'Напиши все новое имя')
            #bot.register_next_step_handler(call.message.chat.id, ch_name1)
            #what_yn_com == 0

    #elif call.data == 'Нет':
        #if what_yn_com == 1:
            #bot.send_message(call.message.chat.id,  'Ну и иди от сюда')
            #what_yn_com == 0

        #elif what_yn_com == 2:
            #bot.send_message(call.message.chat.id,  'Тогда я тебя запомню таким')
            #what_yn_com == 0
    

bot.polling(none_stop=True, interval=0)
