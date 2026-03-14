import streamlit as st
from streamlit_autorefresh import st_autorefresh
import telebot
import requests
import threading
import queue
from datetime import datetime

BOT_TOKEN = "8726049487:AAFr-7C9nfXwfEQz1ymXwT3Fj_62oB5vIjI"  # Add your bot token
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = 8695947788
msg_queue = queue.Queue()

# -------- TELEGRAM BOT -------- #

# Store messages per user
if "user_messages" not in st.session_state:
    st.session_state.user_messages = {}  # {chat_id: [messages]}

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
🆔 ID: <code>{user_id}</code>
"""

    bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML")


@bot.message_handler(func=lambda m: True)
def receive(message):
    user_text = message.text
    chat_id = message.chat.id

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = f"[{time_now}] {chat_id} : {user_text}"

    msg_queue.put((chat_id, msg))  # Store with chat_id

    # Save in a file
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

# -------- PULL MESSAGES FROM QUEUE -------- #
while not msg_queue.empty():
    chat_id, msg = msg_queue.get()
    if chat_id not in st.session_state.user_messages:
        st.session_state.user_messages[chat_id] = []
    st.session_state.user_messages[chat_id].append(msg)

# -------- RECEIVED TAB WITH USER TABS -------- #
with tab2:
    st.subheader("Received Messages")

    if st.session_state.user_messages:
        # Create a tab for each user
        user_tabs = st.tabs([str(uid) for uid in st.session_state.user_messages.keys()])

        for i, chat_id in enumerate(st.session_state.user_messages.keys()):
            with user_tabs[i]:
                for m in reversed(st.session_state.user_messages[chat_id]):
                    st.write(m)
    else:
        st.write("No messages received yet.")

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

        # Add message to session_state for live view
        if int(CHAT_ID) not in st.session_state.user_messages:
            st.session_state.user_messages[int(CHAT_ID)] = []
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.user_messages[int(CHAT_ID)].append(f"[{time_now}] Bot : {MESSAGE}")

        st.success("Message Sent")