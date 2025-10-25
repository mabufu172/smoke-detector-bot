from random import randrange
import discord
import threading

# config
bot_token = 'discord-bot-token-from-discord-dev-apps'
min_beep_delay = 30
max_beep_delay = 60 # According to google, it beeps per 30 to 60 seconds

beep = False

def repeat(trigger):
    if not beep:
        return
    interval = randrange(min_beep_delay, max_beep_delay)
    def func_wrapper():
        repeat(trigger)
        trigger()
    t = threading.Timer(interval, func_wrapper)
    t.start()
    return t

def do_i_beep(yes_or_no):
    global beep
    beep = yes_or_no

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('I\'m online.')

@client.event
async def on_message(message):

    author = message.author
    ctx = message.content
    ch = message.channel

    def playBeep():
        if message.guild.voice_client and beep:
            message.guild.voice_client.play(discord.FFmpegPCMAudio("beep.wav"))
    
    if author == client.user:
        return

    if ctx.startswith('$start'):
        if not beep:
            if author.voice:
                if not message.guild.voice_client:
                    await author.voice.channel.connect()
                do_i_beep(True)
                repeat(playBeep)
                await ch.send('Okay I\'m starting.')
            else:
                await ch.send('I see you\'re not in a voice channel or I can\'t see it.')
        else:
            await ch.send('I\'m already beeping.')

    if ctx.startswith('$stop'):
        if beep:
            do_i_beep(False)
            await ch.send('Okay I\'m stopping.')  
        else:
            await ch.send('You\'ve told me to already.')

    if ctx.startswith('$leave'):
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            do_i_beep(False)
        else: 
            await ch.send("I\'m not in a voice.")

client.run(bot_token)
