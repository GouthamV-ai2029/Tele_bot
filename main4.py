import streamlit as st
from streamlit_autorefresh import st_autorefresh
import telebot
import requests
import threading
import queue
from datetime import datetime

BOT_TOKEN = "8726049487:AAFr-7C9nfXwfEQz1ymXwT3Fj_62oB5vIjI"

bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = 8695947788
msg_queue = queue.Queue()

# -------- TELEGRAM BOT -------- #

@bot.message_handler(commands=['start'])
def start(message):

    user = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    bot.send_message(message.chat.id, "Hey! I am Cipher Bot.")

    admin_msg = f"""
🚀 New User Started Bot

👤 Name: {user}
🔗 Username: @{username}
🆔 ID: {user_id}
"""

    bot.send_message(ADMIN_ID, admin_msg)
@bot.message_handler(func=lambda m: True)
def receive(message):
    user_text = message.text
    chat_id = message.chat.id

    time_now=datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = f"[{time_now}] {chat_id} : {user_text}"

    msg_queue.put(msg)

    with open("messages.txt", "a") as f:
        f.write(msg + "\n")

    print(msg)

def run_bot():
    bot.infinity_polling()

# Start bot only once
if "bot_started" not in st.session_state:
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    st.session_state.bot_started = True

# -------- STREAMLIT UI -------- #

st.title("Telegram Bot Dashboard")
st_autorefresh(interval=2000, key="msg_refresh")

tab1, tab2 = st.tabs(["Send Message", "Received Messages"])

# Initialize session messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Pull messages from queue
while not msg_queue.empty():
    st.session_state.messages.append(msg_queue.get())

# -------- RECEIVED TAB -------- #

with tab2:
    st.subheader("Received Messages")

    try:
        with open("messages.txt", "r") as f:
            messages = f.readlines()

        for m in reversed(messages):
            st.write(m)

    except:
        st.write("No messages received")

# -------- SEND TAB -------- #

with tab1:

    CHAT_ID = st.text_input("Telegram Chat ID")
    MESSAGE = st.text_input("Message")

    if st.button("Send Message"):

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": MESSAGE
        }

        requests.post(url, data=data)

        st.success("Message Sent")