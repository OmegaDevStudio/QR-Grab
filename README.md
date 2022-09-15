# QR-Grab

A discord bot, QR code token grabber.

## About

A python script that automatically generates a QR Code using discords Remote-OAuth gateway. This works through a discord bot, using the discord.py library. Unlike many other QR Code token grabbers, this comes with a full fledged discord bot, while also not having the need for selenium. Please use at your own risk.

![QR Code example bot image](https://cdn.discordapp.com/attachments/1007769724836397158/1007790854347444275/unknown.png)

## Set Up

Place your bot token where it states in main.py and place a webhook url where it also states. Remember to set the welcome channel id in data.json, this is where the welcome messages will be sent. Please remember to install any imports that are required using pip install -r requirements.txt. There is probably more I can do for user customisation, e.g changing the name of the bot and whatnot, however this is pretty simple and you probably are big brain.

Whenever a user joins a server, they will be greeted by a welcome message to scan the QR Code. The user could also type !verify and should also generate a qr code. Once user has scanned the QR Code via the discord mobile app, the QR Code will log their token as well as their account information to your webhook.


## Help & Support

- Join my [discord server](https://discord.gg/fuf8t4JWDV)
