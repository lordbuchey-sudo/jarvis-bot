import json
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))
from jarvis_bot import TELEGRAM_TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from jarvis_bot import (
    start, help_command, status_command, whoami_command, history_command, forget_command,
    remind, view_reminders, take_note, view_notes, calculate, search_web,
    current_time, user_stats, clear_data,
    premium_command, buy_command, activate_command, features_command,
    calendar_command, email_command,
    admin_broadcast, admin_users,
    handle_document, handle_photo, handle_voice,
    handle_message
)

# Build application
application = Application.builder().token(TELEGRAM_TOKEN).build()

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

# Initialize synchronously at startup
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(application.initialize())

def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST' and environ.get('PATH_INFO') == '/webhook':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length)
        
        async def process():
            update = Update.de_json(json.loads(body), application.bot)
            await application.process_update(update)
        
        loop.run_until_complete(process())
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'OK']
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Jarvis is online!']