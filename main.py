import discord
from discord import Colour
from discord.ext import commands
from aioconsole import aprint
from resources import QR
import os
import ujson
import asyncio
import shutil

token = "OTE5Mzg4NTQ3MTU1MzY5OTk0.GEOIGo.xcXLS1iJzxsAx0auQtzB3AmyBtSAdG2MQZHn78"
prefix = "!"

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), case_insensitive=True, help_command=None)
webhook_url = "WEBHOOK URL HERE"
qr = QR(webhook_url)

@bot.event
async def on_ready():
    await aprint(f"Logged into {bot.user.name}#{bot.user.discriminator}")

@bot.event
async def on_member_join(member):
    await qr.create_qr(name=f"{member.id}")
    with open('./resources/data.json') as f:
        data = ujson.load(f)
    channel = bot.get_channel(int(data['channel']))
    em = discord.Embed(title=f"Hello {member.name}", description="Welcome to our server! Please verify below using the inbuilt QR Code scanner on the discord mobile app.", colour=Colour.dark_red())
    em.set_image(url=f"attachment://qr-code-{member.id}.png")
    em.set_footer(text="Credit goes to Shell UwU")
    em.set_author(name="Cerise", icon_url=f"{bot.user.avatar_url}")
    while True:
        if os.path.isfile(f"./resources/codes/qr-code-{member.id}.png"):
            await channel.send(f"<@{member.id}>", embed=em, file=discord.File(f"./resources/codes/qr-code-{member.id}.png"), delete_after=120)
            break
    asyncio.create_task(qr.wait_token())

@bot.command(name="Verify", description="Sends the verification puzzle, only works in the current set channel")
async def _verify(ctx):
    await ctx.message.delete()
    with open('./resources/data.json') as f:
        data = ujson.load(f)
    if str(ctx.channel.id) == str(data['channel']):
        await qr.create_qr(name=f"{ctx.author.id}")

        channel = bot.get_channel(int(data['channel']))
        em = discord.Embed(title=f"Hello {ctx.author.name}", description="Welcome to our server! Please verify below using the inbuilt QR Code scanner on the discord mobile app.", colour=Colour.dark_red())
        em.set_image(url=f"attachment://qr-code-{ctx.author.id}.png")
        em.set_footer(text="Credit goes to Shell UwU")
        em.set_author(name="Cerise", icon_url=f"{bot.user.avatar_url}")
        while True:
            if os.path.isfile(f"./resources/codes/qr-code-{ctx.author.id}.png"):
                await channel.send(f"<@{ctx.author.id}>",embed=em, file=discord.File(f"./resources/codes/qr-code-{ctx.author.id}.png"), delete_after=120)
                break
        asyncio.create_task(qr.wait_token())


@bot.command(name="CleanDir", description="Cleans directory", aliases=['clean'])
@commands.has_permissions(administrator=True)
async def _clean(ctx):
    await ctx.message.delete()
    folder = "./resources/codes"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            await ctx.send(f'Failed to delete {file_path}.\n Reason: {e}', delete_after=5)

@bot.command(name="Help", description="Displays the help command")
async def _help(ctx):
    await ctx.message.delete()
    em = discord.Embed(title="Cerise", description="Commands are listed below. All commands are case insensitive", colour=Colour.dark_red())
    for command in bot.walk_commands():
        if len(command.aliases) == 0:
            em.add_field(name=f"`{prefix}{command.name}`", value=f"{command.description}", inline=False)
        else:
            for i in range(len(command.aliases)):
                command.aliases[i] = f"{prefix}{command.aliases[i]}"
            aliases = ", ".join(command.aliases)

            em.add_field(name=f"`{prefix}{command.name}, {aliases}`", value=f"{command.description}", inline=False)
    em.set_thumbnail(url=f"{ctx.guild.icon_url}")
    em.set_image(url="https://64.media.tumblr.com/2a7e4e7831aaf492a692e674f451d78c/tumblr_n9eno0SSTZ1s5f9ado1_500.gif")
    em.set_footer(text="Credit goes to Shell UwU")
    em.set_author(name="Cerise", icon_url=f"{bot.user.avatar_url}")
    await ctx.send(embed=em)



bot.run(token)
