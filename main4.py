import streamlit as st
import telebot
st.title("TelegramBotHosting")
TOKEN = "8748531687:AAG8cQiy95YB_lRMxp5AofzcMv6FxV1plxM"
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot is hosting through streamlit")

bot.polling()
