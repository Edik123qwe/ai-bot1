import telebot, os, random
from bot_logic import gen_pass, coin, get_duck_image_url, get_class

# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot('8447372362:AAH2KnmEJ1SEs8tSOyKzhKPMlznJkHiiMZg')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Привет! Я бот {bot.get_me().first_name}!/start /heh /hello /mem /orelandreshka /bye /password /duck /emj')


@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)


@bot.message_handler(commands=['hello'])
def send_hello(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"Привет, {name}! Как дела?")


@bot.message_handler(commands=['orelandreshka'])
def send_orelandreshka(message):
    bot.reply_to(message, coin())


@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")


@bot.message_handler(commands=['password'])
def send_password_to(message):
    bot.reply_to(message, f'ваш сгенерированый пароль: {gen_pass(10)}')

@bot.message_handler(commands=['mem'])
def send_mem(message):
    random_img = random.choice(os.listdir('images'))
    with open(f'images/{random_img}', 'rb') as f:
        bot.send_photo(message.chat.id, f)
@bot.message_handler(commands=['emj'])
def emoji(message):
    emogi = '😒😍🤣😂😊❤️👌💕😘😁🙌👍'
    random_emogi = random.choice(emogi)
    bot.reply_to(message, random_emogi)
@bot.message_handler(commands=['duck'])
def duck(message):
    '''По команде duck
     вызывает функцию get_duck_image_url
     и отправляет URL изображения утки'''
    image_url = get_duck_image_url()
    bot.reply_to(message, image_url)

@bot.message_handler(content_types=['photo'])
def photo(message):
    if not message.photo:
        return  bot.send_message(message.chat.id,'картинка не загрузилась')
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = get_class(model_path="keras_model.h5", labels_path='labels.txt', image_path="file_name")
    bot.send_message(message.chat.id, result)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
