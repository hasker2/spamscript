from pyrogram import Client, filters
import random
from pyrogram.errors import FloodWait
import time
import sqlite3 as sl
import configparser
from userconfig import *
import os

print('getting channel ids')
with sl.connect('channelids.db', check_same_thread=False) as con:
    cur = con.cursor()
    rows = cur.execute('select ids from channelids')
    channelids = rows.fetchall()
    channels = []
    for row in channelids:
        for id in row:
            channels.append(id)
    print(channels)

print('getting texts')
with sl.connect('texts.db', check_same_thread=False) as con:
    cur = con.cursor()
    rows = cur.execute('select text from texts')
    spamtext = rows.fetchall()
    spam = []
    for row in spamtext:
        for text in row:
            spam.append(text)
    print(spam)

print('''
░██████╗██████╗░░█████╗░███╗░░░███╗░██████╗░█████╗░██████╗░██╗██████╗░████████╗
██╔════╝██╔══██╗██╔══██╗████╗░████║██╔════╝██╔══██╗██╔══██╗██║██╔══██╗╚══██╔══╝
╚█████╗░██████╔╝███████║██╔████╔██║╚█████╗░██║░░╚═╝██████╔╝██║██████╔╝░░░██║░░░
░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║░╚═══██╗██║░░██╗██╔══██╗██║██╔═══╝░░░░██║░░░
██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██████╔╝╚█████╔╝██║░░██║██║██║░░░░░░░░██║░░░
╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░''')
print('\nMy GitUb - https://github.com/hasker2\n\nScript GitUb - https://github.com/hasker2/SpamScript')

app = Client("my account", api_id=api_id, api_hash=api_hash)


@app.on_message(filters.command("help") & filters.me)
def help(_, message):
    print(popup)
    message.reply_text('Firstly you shoud join to channel chat (tutorial video upper)\nSecondary you should enter .newchannel and channel ')

#----------------
#channel commands
#----------------

@app.on_message(filters.command("newchannel") & filters.me)
def addnewchannel(_, message):
    #app.delete_messages(chat_id=message.chat.id, message_ids=message.id, revoke=True)
    channelid = message.text.split("/newchannel ", maxsplit=1)
    try:
        channelid = channelid[1]
        time.sleep(0.5)
        if channelid[0] == '-':
            message.reply_text('Your new channel id: ' + channelid)
            try:
                with sl.connect('channelids.db', check_same_thread=False) as con:
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO channelids VALUES ('{int(channelid)}')")
            except:
                pass
            channels.append(int(channelid))
            print(channels)
        else:
            message.reply_text('Enter your channel id after space, example: "/newchannel -12345678910"')
    except:
        message.reply_text('Enter your channel id after space, example: "/newchannel -12345678910"')

@app.on_message(filters.command("clearchannels") & filters.me)
def clearchannels(_, message):
    channels.clear()
    try:
        with sl.connect('channelids.db', check_same_thread=False) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM channelids WHERE ids != 0")
    except:
        pass
    message.reply_text('Channels list cleared')

@app.on_message(filters.command("removechannel") & filters.me)
def removechannel(_, message):
    channelid = message.text.split("/removechannel ", maxsplit=1)
    try:
        channelid = channelid[1]
        time.sleep(0.5)
        if channelid[0] == '-':
            message.reply_text('You want remove channel with id: ' + channelid)
            try:
                with sl.connect('channelids.db', check_same_thread=False) as con:
                    cur = con.cursor()
                    cur.execute(
                        f"DELETE FROM channelids WHERE ids={int(channelid)}")
            except:
                pass
            print(channels)
        else:
            message.reply_text('Enter your channel id after space, example: "/removechannel -12345678910"')
    except:
        message.reply_text('Enter your channel id after space, example: "/removechannel -12345678910"')

#----------------
#text commands
#----------------

@app.on_message(filters.command("newtext") & filters.me)
def newtext(_, message):
    spamtext = message.text.split("/newtext ", maxsplit=1)
    spamtext = spamtext[1]
    message.reply_text('Your text: ' + spamtext)
    try:
        with sl.connect('texts.db', check_same_thread=False) as con:
            cur = con.cursor()
            cur.execute(
                f"INSERT INTO texts VALUES ('{str(spamtext)}')")
    except:
        pass

@app.on_message(filters.command("cleartexts") & filters.me)
def cleartexts(_, message):
    spam.clear()
    try:
        with sl.connect('channelids.db', check_same_thread=False) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM texts WHERE text != Null")
    except:
        pass

#----------------
#posting commands
#----------------

@app.on_message(filters.channel)
def channelcheck(_, message):
    if message.sender_chat.id in channels:
        print(f'Trying to post spam in "{message.sender_chat.title}" channel comments')
        try:
            m = app.get_discussion_message(message.sender_chat.id, message.id)
            m.reply(random.choice(spam))
        except Exception as err:
            print('ERROR:' + err)
        print(f'Spam was posted in "{message.sender_chat.title}" channel comments')

app.run()