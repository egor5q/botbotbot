# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
import calendar
import test
import time
import traceback
from telebot import types
from emoji import emojize
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
randlist=['Возбужденный самец', 'Веган', 'Большой Банан', 'Гей Воробей', 'Большая Залупа Коня', 'Малая Залупа Коня', 'Осёл', 
         'Дрочила', 'Дрочемыш', 'Анальный Зонд', 'Гей',
         'Анальный зверь']
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    if call.data=='join':        
      try:
        if call.from_user.id not in info.lobby.game[call.message.chat.id]['players']:
              z=0
              for ids in info.lobby.game:
                  if call.from_user.id in info.lobby.game[ids]['players']:
                    z+=1    
              if z==0:
               if len(info.lobby.game[call.message.chat.id]['players'])<len(randlist):
                  info.lobby.game[call.message.chat.id]['players'].update(createuser(call.from_user.id, call.message.chat.id))
                  bot.send_message(call.message.chat.id, 'Аноним вошел!')
                  info.lobby.alreadyplay.append(call.from_user.id)
               else:
                   try:
                       bot.send_message(call.from_user.id, 'Достигнуто максимальное число пидоров!')
                   except:
                       pass
                    
               #if len(info.lobby.game[call.message.chat.id]['players'])>len(randlist):
               # bot.send_message(call.message.chat.id, 'Набор окончен!')
               # begin(call.message.chat.id)
      except:
        pass
                                  


def del2(id):
    try:
      del info.lobby.game[id]
      bot.send_message(id, '24 часа прошло! Вирт остановлен!')
    except:
      pass

def delplayer(id, id2):
    try:
        del info.lobby.game[id]['players'][id2]
    except:
        pass
            
def deleter(id):
  try:
    del info.lobby.game[id]
  except:
    pass
    
@bot.message_handler(commands=['stop'])
def s(m):
  for ids in info.lobby.game:
    if m.from_user.id in info.lobby.game[ids]['players']:
        bot.send_message(ids, 'Аноним вышел!')
        t=threading.Timer(0.1, delplayer, args=[ids, m.from_user.id])
        t.start()

@bot.message_handler(commands=['lobby'])
def m(m):
    if m.chat.id not in info.lobby.game:
        info.lobby.game.update(createroom(m.chat.id))
        #t=threading.Timer(999999, del2, args=[m.chat.id])
        #t.start()
        #info.lobby.game[m.chat.id]['timer']=t
        bot.send_message(441399484, 'Вирт начался где-то!')
        Keyboard=types.InlineKeyboardMarkup()          
        Keyboard.add(types.InlineKeyboardButton(text='Кнопка', callback_data='join'))
        info.lobby.game[m.chat.id]['startm']=bot.send_message(m.chat.id, 'Начинаем! жмите на кнопку, чтобы присоединиться', reply_markup=Keyboard)
    else:
      try:
        bot.reply_to(info.lobby.game[m.chat.id]['startm'], 'Вирт уже идёт!')
      except:
        pass

def namechoice(id):
    x=random.choice(randlist)
    while x in info.lobby.game[id]['nicks']:
        x=random.choice(randlist)
    info.lobby.game[id]['nicks'].append(x)
    return x
        
        
def begin(id):
    pass
    #for ids in info.lobby.game[id]['players']:
    #  try:
    #    bot.send_message(ids, 'Пишите сюда что то')
    #  except:
    #    bot.send_message(id, 'Какой то пидорас не открыл диалог с ботом!')
 
@bot.message_handler(commands=['xyeta'])
def mutee(m):
    print (calendar.monthrange(2012,1)[1])
    if m.chat.id!=m.from_user.id:
      try:
        member=bot.get_chat_member(m.chat.id, m.from_user.id)
        if member.status=='administrator' or member.status=='creator':
            text=m.text.split(' ')
            try:
                timee=text[1]
                i=int(timee[:-1])
                number=timee[len(timee)-1]
            except:
                i=0
                number='m'
            
            untildate=int(time.time())
            if number=='m':
                untildate+=i*60
                datetext='сисяк'
            if number=='h':
                untildate+=i*3600
                datetext='больших сисяк'
            if number=='d':
                untildate+=i*3600*24
                datetext='гигантских сисяк'
                           
            print(untildate)
            
            if m.reply_to_message!=None:
                bot.restrict_chat_member(can_send_messages=False, user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id, until_date=untildate)
                if i==0:
                    text='Замутил навсегда.'
                else:
                    text='Замутил на '+str(i)+' '+datetext+'.'
                bot.send_message(m.chat.id, text)
        else:
            bot.send_message(m.chat.id, 'Ты кто такой сука чтобы это делать?')
      except Exception as e:
        bot.send_message(m.chat.id, 'Ошибка мута.')

            

@bot.message_handler(commands=['ne_xyeta'])
def unmutee(m): 
  if m.chat.id!=m.from_user.id:
      try:
        member=bot.get_chat_member(m.chat.id, m.from_user.id)
        if member.status=='administrator' or member.status=='creator':
            bot.restrict_chat_member(can_send_messages=True, user_id=m.reply_to_message.from_user.id, chat_id=m.chat.id)
            bot.send_message(m.chat.id, 'Размутил.')
        else:
            bot.send_message(m.chat.id, 'Ты кто такой сука чтобы это делать?')
      except:
          bot.send_message(m.chat.id, 'Ошибка.')
         


@bot.message_handler(content_types=['text'])
def h(m):
    for ids in info.lobby.game:
        if m.from_user.id in info.lobby.game[ids]['players']:
          if m.chat.id>0:
            try:
              bot.send_message(ids, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
              info.lobby.game[ids]['timer'].cancel()
              t=threading.Timer(1500, del2, args=[ids])
              t.start()
              info.lobby.game[ids]['timer'].stop()
              info.lobby.game[ids]['timer']=t
            except:
                pass
            try:
                for idd in info.lobby.game[ids]['players']:
                    if m.from_user.id!=idd:
                      bot.send_message(idd, '_'+info.lobby.game[ids]['players'][m.from_user.id]['name']+'_:\n'+m.text, parse_mode='markdown')
            except:
                pass

    
def createroom(id):
  return{id:{
      'nicks':[],
      'startm':None,
      'timer':None,
    'players':{
    }
     }
      }   
        
def createuser(id, chatid):
    return{id:{
           'name':namechoice(chatid)
          }
          }
       
       
       
       
if __name__ == '__main__':
  bot.polling(none_stop=True)



