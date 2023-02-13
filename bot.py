import telegram
import requests
import json
import time


print('bot is starting...')
time.sleep(2)

# enter below your telegram bot token you find in the "botfather".
bot = telegram.Bot(token='6208841109:AAGyetSzKfU_7dCbkGEcyuoGOa1VZ0iHaBs')
print("API loaded correctly...")

# function responsible for take by API coin price you want to get to know.
def get_price(symbol):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        if "USD" in data:
            return data["USD"]
        else:
            return None
    else:
        return None

# function that takes your message from telegram e.g if you write /eth function takes it and send it to the symbol.
def handle_message(bot, update):
    if update.message:
        message = update.message.text
        if message.startswith("/"):
            symbol = message.split(" ")[0][1:].upper()
            price = get_price(symbol)
            if price:
                bot.send_message(chat_id=update.message.chat_id, text=f"{symbol} ${price}")
                print(f"{symbol} ${price}")
            else:
                bot.send_message(chat_id=update.message.chat_id, text=f"Sorry, I couldn't find the coin you wrote, please write again correctly")
        else:
            pass

# main function.
# remember if bot at the start printing "Timed out, trying again..." please remove your bot from a telegram group. 

def main():
    time.sleep(2)
    update_id = None
    waiting_time = 60
    start_time = time.time()
    while True:
        try:
            updates = bot.get_updates(offset=update_id)
            if updates:
                for update in updates:
                    handle_message(bot, update)
                    update_id = update.update_id + 1
            else:
                if time.time() - start_time >= waiting_time:
                    start_time = time.time()
                    print("No new updates, waiting for a message...")
        except:
                if time.time() - start_time >= waiting_time:
                    start_time = time.time()
                    print("Timed out, trying again...")

if __name__ == '__main__':
    main()
