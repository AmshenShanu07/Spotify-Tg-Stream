from stream import app, tgCall
from pyrogram.types import Message
from pytgcalls.types import Update
from pyrogram import Client, filters
from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError, GroupCallNotFound

import os
import time
import random
from subprocess import check_output


global index
global userFilter


sudo_users = [885866704, 6102667313, 1209597031]


# 6102667313
# 885866704
@app.on_message(filters.group & filters.user(sudo_users) & filters.command("start"))
async def start_handler(bot:Client,event:Message):
    try:
        await tgCall.join_group_call(event.chat.id, stream=AudioPiped('./song.mp3'))
        await tgCall.change_volume_call(event.chat.id,100)
        await tgCall.pause_stream(event.chat.id)

        await event.reply(text="Ready to play the song!")
        time.sleep(3)
        await event.delete()
        
    except NoActiveGroupCall:
        await event.reply(text="Have no permission in this chat!")
        time.sleep(3)


# -1001938777292
@app.on_message(filters.group & filters.user(sudo_users) & filters.command("play"))
async def play_handler(bot:Client, event:Message):
    try:
        songIndex = int(event.text.replace('/play ',''))
        downloaded_songs = os.listdir('./songs/playlist')

        songsList = os.listdir('./songs/playlist')
        songsList = [song.split(' - ')[1] for song in songsList]
        songsList.sort()

        for i in range(len(downloaded_songs)):
            if songsList[songIndex-1] in downloaded_songs[i]:
                index = i;
        
        time.sleep(3)
        await event.reply(f"Now Playing...\n\n{downloaded_songs[index]}")
        await tgCall.resume_stream(event.chat.id)
        await tgCall.change_stream(event.chat.id,stream=AudioPiped(f'./songs/playlist/{downloaded_songs[index]}'))
    
    except ValueError:
        downloaded_songs = os.listdir('./songs/playlist')
        song = random.choice(downloaded_songs)
        await event.reply(event.chat_id,text=f"Now Playing...\n\n{song}")
        time.sleep(3)
        await tgCall.change_stream(event.chat_id,stream=AudioPiped(f'././songs/playlist/{song}'))

    except NoActiveGroupCall:
        await event.reply(text="Have no permission in this chat!")
        time.sleep(3)
        await event.delete()

    except NotInGroupCallError:
        await event.reply(text="Stremming not found!")
        time.sleep(3)
        await event.delete()

    except GroupCallNotFound:
        await event.reply(text="Stream Not Found!")
        await event.delete()



@app.on_message(filters.group & filters.user(sudo_users) & filters.command("download"))
async def download_song(bot:Client, event:Message):
    url = event.text.replace('/download ','')

    if url == '/download':
        await event.reply("plzz provide a url")
        return
    
    await event.reply("Please wait downloding on progress..")
    log = check_output(['spotdl', url, '--output', './songs/playlist'])
    await event.reply(log)
    


@app.on_message(filters.group & filters.user(sudo_users) & filters.command("songs"))
async def get_all_songs(bot:Client,event:Message):
    songsList = os.listdir('./songs/playlist')
    songsList =[song.split(' - ')[1] for song in songsList]
    songsList.sort()
    songsListText =''
    for i in range(len(songsList)):
        song = songsList[i]
        songsListText += f'{i+1})  {song}\n'

    await event.reply(text=songsListText)



@app.on_message(filters.group & filters.user(sudo_users) & filters.command("stop"))
async def get_details(bot:Client,event:Message):
    await tgCall.leave_group_call(event.chat.id)
    await event.reply("Stream Stopped Successfully!")




@app.on_message(filters.command("sudo") & filters.me)
async def get_details(bot:Client,event:Message):
    if(event.reply_to_message):
        print(event.reply_to_message.from_user.id)



@app.on_message(filters.command("getsudo"))
async def get_details(bot:Client,event:Message):
    msg = "\n\n bla  bla \n\n bla"
    await event.reply(msg)



@tgCall.on_stream_end()
async def onStreamEnd(bot:Client,event:Update):
    downloaded_songs = os.listdir('./songs/playlist')
    song = random.choice(downloaded_songs)
    await app.send_message(event.chat_id,text=f"Now Playing...\n\n{song}")
    time.sleep(3)
    await tgCall.change_stream(event.chat_id,stream=AudioPiped(f'././songs/playlist/{song}'))


tgCall.run()
