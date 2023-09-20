
import schedule
import requests
from bs4 import BeautifulSoup


from config import token, chat_id

slip_tim = 86400  # 86400 сутки
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

link = 'https://www.zarseti.ru/Home'


def tg_get(data_g):
    message = data_g
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()  # Эта строка отсылает сообщение


def get():
    data_g = ''
    try:
        response = requests.get(url=link, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        data_gs = soup.find_all('div', class_='Blackouts')
        for data_i in data_gs:
            data_g = data_g + data_i.text
        if 'заринск' in data_g.lower():
            tg_get(data_g)
        else:
            tg_get('По Голухе нет завтра отключений')

    except Exception as ex:
        print(ex)
    finally:
        data_g = ''


def main():
    schedule.every().day.at('15:08').do(get)
    # schedule.every(4).seconds.do(get)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
