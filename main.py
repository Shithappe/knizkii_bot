import telebot
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def escape_reserved_characters(input_string):
    reserved_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in reserved_characters:
        input_string = input_string.replace(char, f'\\{char}')
    
    return input_string

bot = telebot.TeleBot('6404783555:AAE_CqT5J9f-oWP_Iaxly-Hx9DjU19DYSm0')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}. Что почитаем?')

@bot.message_handler()
def main(message):

    search_query = message.text
    encoded_query = quote(search_query, safe='')

    url = f'https://flibusta.site/booksearch?ask={encoded_query}&chb=on'


    response = requests.get(url)

    if response.status_code != 200:
        print(f'Запрос завершился с ошибкой. Код статуса: {response.status_code}')

    html = response.text




    soup = BeautifulSoup(html, 'html.parser')



    ul_tags = soup.find_all('ul')
    big_ul = 'None'


    if len(ul_tags) > 1:
        if ul_tags[1].get_text().find('1') < 0:
            big_ul = str(ul_tags[1])

        else: 
            big_ul = str(ul_tags[2])
    
    else:
        print("Второй тег <ul> не найден.")

    links_data = []

    if big_ul:

        soup = BeautifulSoup(big_ul, 'html.parser')
        li_elements = soup.find_all('li')


        # Проходимся по каждому элементу <li> и извлекаем информацию о ссылках
        for li_element in li_elements:
            a_tags = li_element.find_all('a')  # Находим все теги <a> внутри элемента <li>
            
            if len(a_tags) >= 2:
                link_title = f'{a_tags[0].get_text()}  { a_tags[1].get_text()}'  # Получаем текст первой ссылки
                link_url = a_tags[0]['href']  # Получаем URL первой ссылки
                
                data = {
                    'title': link_title,
                    'url': link_url
                }
                
                links_data.append(data)

        result_string = "Вот что я нашел:\n\n"

        if links_data:

            # Выводим данные о ссылках
            for link_data in links_data:
                # result_string += f"[{escape_reserved_characters(link_data['title'])}](https://flibusta.site{link_data['url']}/fb2)\n\n"
                result_string += f"{escape_reserved_characters(link_data['title'])}\n[fb2](https://flibusta.site{link_data['url']}/fb2)   [epub](https://flibusta.site{link_data['url']}/epub)\n\n"
        
        else:
            result_string = f"По данному запросу я ничего не смог найти \\:\\'\\( \nПроверьте правильность запроса\\."



    bot.send_message(message.chat.id, f'{result_string}', parse_mode='MarkdownV2')



    # file_url = 'https://flibusta.site//b/102773/fb2'

    # # Отправляем GET-запрос для загрузки файла
    # response = requests.get(file_url)

    # # Проверяем статус код ответа
    # if response.status_code == 200:
    #     # Открываем локальный файл для записи бинарных данных
    #     with open('downloaded_file.fb2', 'wb') as file:
    #         file.write(response.content)
    #     print('Файл успешно скачан.')
    # else:
    #     print(f'Ошибка при скачивании. Код статуса: {response.status_code}')

bot.infinity_polling()

