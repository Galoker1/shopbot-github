import telebot
from telebot import types
from requests import get
buy=[0,0,0]
bot=telebot.TeleBot('token')
items=[
    ["Лапша Биг Ланч Курица",7,20,"https://sun9-8.userapi.com/impg/cpxoowDnIHJZV0NtIyL82PDO--tl-FxiV6wbOw/5zYe83c6EWo.jpg?size=768x1024&quality=96&sign=152f1346edb3e58decb0ee7b16dbc1cf&type=album"],
    ["Лапша Биг Ланч Говядина",9,20,"https://sun9-56.userapi.com/impg/PcMD78s4MNZO9ndz9MIc--UlQXt9wlvbbiilNA/51U4Cj6hdNc.jpg?size=768x1024&quality=96&sign=417d43c77df42dfb69405372d859e6f3&type=album"],
    ["Энергетик Jaguar",29,45,"https://sun9-63.userapi.com/impg/tv5fNiin4OyKBEL_-1Y59MtRucS0t6csZZkl4Q/knqy5yBKISA.jpg?size=768x1024&quality=96&sign=f0eefaf977055d829bb2068d675a9fe6&type=album"],
    ["Сухарики Воронцовские 500гр",6,120,"https://sun9-8.userapi.com/impg/m-lpJ2XdazUPYdMGN4xtIFyY8bauRsgn0LAgkg/HgwY-IUSAr0.jpg?size=768x1024&quality=96&sign=f5a3e6d280da91ab47956bbbc7458723&type=album"]
    ]
buttons=[]
usrs=[]
dict={417081307: [0, 2, 0]}

def check_user(id):
    if id not in usrs:
        usrs.append(id)
        dict[id]=[0,0,0]
def clear_cart(id):
    dict[id]=[0,0,0]


#add_name_many_cash_photo
#change_number_many
#delete_number
@bot.message_handler(commands=['start'])

def welcome(message):
    check_user(message.chat.id)
    clear_cart(message.chat.id)
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    item1 = types.KeyboardButton("Магазин")
    markup1.add(item1)
    bot.send_message(message.chat.id, "<b>Магазин 5ЛЕТ</b>\nДля заказа нужно перейти во вкладку Магазин\nОплата при получении",parse_mode='html', reply_markup=markup1)

@bot.message_handler(content_types=['text'])
def send(message):

    if message.text=="Магазин":
        check_user(message.chat.id)
        clear_cart(message.chat.id)
        buttons.clear()
        markup = types.InlineKeyboardMarkup(row_width=1)
        if len(buttons)==0:
            for item in items:
                if item[1]!=0:
                    buttons.append(types.InlineKeyboardButton(item[0]+"-"+str(item[2])+"₽"+"("+str(item[1])+"шт)", callback_data="inf_"+str(items.index(item))))
            for button in buttons:
                markup.add(button)
        bot.send_message(message.chat.id, 'Выбирай что захочешь ни в чем себе не отказывай', reply_markup=markup)
    if str(message.chat.id)=="417081307":
        try:
            msg=str(message.text).split("_")
            if msg[0]=="get":
                bot.send_message("417081307", str(items))
            if msg[0]=="add":
                items.append([msg[1],int(msg[2]),int(msg[3]),msg[4]])
                buttons.clear()
            if msg[0]=="change":
                items[int(msg[1])][1]=msg[2]
                buttons.clear()
            if msg[0]=="delete":
                del items[int(msg[1])]
                buttons.clear()
        except:
            bot.send_message("417081307", "Неверная команда")


def many(message):
    print("&&&&&")
    print(dict)
    try:
        dict[message.chat.id][1]=int(message.text)

        many=dict[message.chat.id][1]
        if int(many)<=int(items[dict[message.chat.id][0]][1]) and int(many)>0:
            bot.send_message(message.chat.id, "Введите номер комнаты")
            print("?????")
            print(dict)
            bot.register_next_step_handler(message,room)

        else:
            bot.send_message(message.chat.id, "Возможно вы ввелли некоректное кол-во")

    except:
        bot.send_message(message.chat.id, "Возможно вы ввелли некоректное кол-во")
        clear_cart(message.chat.id)


def room(message):
    try:
        dict[message.chat.id][2]=int(message.text)
        many=dict[message.chat.id][1]
        if int(many)<=int(items[dict[message.chat.id][0]][1]):
            bot.send_message(message.chat.id, "Заказ создан:\n"+ str(items[dict[message.chat.id][0]][0]) + " \n" + str(dict[message.chat.id][1]) + "шт" + " \nв комнату: " + str(dict[message.chat.id][2]) + "\n" + str(items[dict[message.chat.id][0]][2]*dict[message.chat.id][1])+"₽")
            markup2 = types.InlineKeyboardMarkup(row_width=2)
            markup2.add(types.InlineKeyboardButton("OK", callback_data=str(message.chat.id)+"_yes" + "_" + str(dict[message.chat.id][1]) + "_" + str(dict[message.chat.id][1])),types.InlineKeyboardButton("NO", callback_data=str(message.chat.id)+"_no" ))
            bot.send_message("417081307", "Заказ создан:\n"+ str(items[dict[message.chat.id][0]][0]) + " \n" + str(dict[message.chat.id][1]) + "шт" + " \nв комнату: " + str(dict[message.chat.id][2]) + "\n" + str(items[dict[message.chat.id][0]][2]*dict[message.chat.id][1])+ "₽")
            bot.send_message("417081307",  str(message.chat.id) + ":" + str(items[dict[message.chat.id][0]][0]) + ":" + str(dict[message.chat.id][1]) + ":" + str(dict[message.chat.id][2]) + ":" + str(items[dict[message.chat.id][0]][2]*dict[message.chat.id][1]) ,reply_markup=markup2)
            print("*****")
            print(dict)
        else:
            bot.send_message(message.chat.id,"Что-то пошло не так. Попробуйте снова")
            clear_cart(message.chat.id)

    except:
        clear_cart(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    ms=call.data.split("_")
    if str(ms[0])=="inf":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="В наличии " + str(items[int(ms[1])][1]) + "шт",reply_markup=None)
        markup3 = types.InlineKeyboardMarkup(row_width=1)
        markup3.add(types.InlineKeyboardButton("Заказать", callback_data="buy_"+str(ms[1])))
        bot.send_photo(call.message.chat.id, get(items[int(ms[1])][3]).content)
        bot.send_message(call.message.chat.id,"------------", reply_markup=markup3)

    if str(ms[0])=="buy":
        print("!!!!!")
        print(dict)
        x=int(ms[1])
        dict[call.message.chat.id][0]=int(ms[1])
        print("----")
        print(dict)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Выберите кол-во",reply_markup=None)
        bot.register_next_step_handler(call.message,many)
    if str(ms[1])=="yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Подтвержден",reply_markup=None)
        bot.send_message(int(call.data.split("_")[0]),"Заказ подтвержден\n Сбер,ВТБ:")
        items[int(dict[call.message.chat.id][0])][1]-=int(dict[int(ms[0])][1])

    elif str(ms[1])=="no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Отменен",reply_markup=None)
        bot.send_message(int(call.data.split("_")[0]),"Заказ отклонен. Попробуйте позже")



bot.polling(none_stop=True)
