import json
import os
from jarvis_bot import TELEGRAM_TOKEN
from jarvis_bot import main as setup_handlers
from telegram import Update
from telegram.ext import Application

# Build the application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Register all handlers (same as your main function)
from handlers.basic import start, help_command, current_time, user_stats, status_command, whoami_command, history_command, forget_command, clear_data
from handlers.productivity import remind, view_reminders, take_note, view_notes, calculate, search_web
from handlers.documents import handle_document
from handlers.media import handle_photo, handle_voice
from handlers.premium import premium_command, buy_command, activate_command, features_command
from handlers.calendar import calendar_command
from handlers.email import email_command
from handlers.admin import admin_broadcast, admin_users
from handlers.chat import handle_message
from telegram.ext import CommandHandler, MessageHandler, filters

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("status", status_command))
application.add_handler(CommandHandler("whoami", whoami_command))
application.add_handler(CommandHandler("history", history_command))
application.add_handler(CommandHandler("forget", forget_command))
application.add_handler(CommandHandler("remind", remind))
application.add_handler(CommandHandler("reminders", view_reminders))
application.add_handler(CommandHandler("note", take_note))
application.add_handler(CommandHandler("notes", view_notes))
application.add_handler(CommandHandler("calc", calculate))
application.add_handler(CommandHandler("search", search_web))
application.add_handler(CommandHandler("time", current_time))
application.add_handler(CommandHandler("stats", user_stats))
application.add_handler(CommandHandler("clear", clear_data))
application.add_handler(CommandHandler("premium", premium_command))
application.add_handler(CommandHandler("buy", buy_command))
application.add_handler(CommandHandler("activate", activate_command))
application.add_handler(CommandHandler("features", features_command))
application.add_handler(CommandHandler("calendar", calendar_command))
application.add_handler(CommandHandler("email", email_command))
application.add_handler(CommandHandler("broadcast", admin_broadcast))
application.add_handler(CommandHandler("users", admin_users))
application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Initialize application
application.initialize()

# WSGI app for webhook
def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/webhook':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length)
        
        update = Update.de_json(json.loads(body), application.bot)
        application.process_update(update)
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Jarvis is online!']