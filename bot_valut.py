# pyTelegramBotAPI
import telebot
from utility import keys, TOKEN
from extensions import ConvertionException, valute

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    text = 'Чтобы начать работу введите команду боту: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Команды: \nvalues - доступные валюты'
    bot.send_message(message.from_user.id, text)

@bot.message_handler(commands=['values'])
def send_valutes(message):
    text = 'Доступные валюты: \n'
    for key, value in keys.items():
        text += f'{key} \n'
    bot.send_message(message.from_user.id, text)

    
@bot.message_handler(content_types=['text'])
def function_input(message):
    values = message.text.split()
    
    try:
        if len(values) != 3:
            raise ConvertionException('Необходимо ввести три параметра')
        
        quote, base, amount = values
    
        text = valute(base, quote, amount).convert()
    except ConvertionException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Технические проблемы {e}')
    else:
        bot.reply_to(message, text)

bot.polling(none_stop=True)
