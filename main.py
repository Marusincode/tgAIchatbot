from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

#bot credentials
TOKEN: Final = "8035633752:AAE4Vbh0NBt4XZUVcbx3Dlx2YbIEb5VP_UM"
botusername: Final = "@maryslamabot"

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am your AI assistant. Ask me anything")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please ask a question for me to answer")

#tinyllama
template = """
Answer the question below.

Question: {question}

Answer:
"""
model = OllamaLLM(model = "tinyllama")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

#responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    result = chain.invoke({"question": processed})
    return result

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

#main
if __name__ == '__main__':
    print("starting bot.....")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(error)

    #poll the bot
    print("Polling....")
    app.run_polling(poll_interval = 3)