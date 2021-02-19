import discord
import os
import requests
import json
import random
from replit import db
import userdata
import time
from discord.ext import tasks
from keep_alive import keep_alive
client = discord.Client()

jh = {
    'x-rapidapi-key': "3e3b3b108amsh634f6f74abdac28p1b33a3jsndbe9079f48eb",
    'x-rapidapi-host': "jokeapi.p.rapidapi.com"
}

sh = {
    'x-rapidapi-key': "07e4f878fdmsh8a653e7caf8b089p1587afjsneb326fd7f412",
    'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
}

game = int(0)

if "responding" not in db.keys():
	db["responding"] = True


def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]["q"] + " -" + json_data[0]["a"]
	return (quote)


def get_joke():
	response = requests.request("GET",
	                            "https://v2.jokeapi.dev/joke/Any",
	                            headers=jh,
	                            params={"format": "json"})
	json_data = json.loads(response.text)
	joke = json_data
	if joke["type"] == "single":
		return (joke["joke"])
	else:
		new = joke["setup"] + "\n" + joke["delivery"]
		return new


loop = [get_quote(), get_joke()]


@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

	if message.author == client.user:
		return

	global game

	word = message.content

	if word == "T&D":
		if game == 0:
			await message.channel.send("*****lets play TND!!!!*****")
			await message.channel.send("Truth or Dare")
			game = 1

	if game == 0:
		msg = word
		td = "none"
	elif game == 1:
		td = word
		msg = "none"

	if msg == "inspire":
		quote = get_quote()
		await message.channel.send(quote)

	if msg == "joke":
		await message.channel.send(get_joke())

	if msg == "khushi":
		"await message.channel.send(file=discord.File('images/khushi.jpg'))"
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('Oye Dibbiya, \n gm babu, Koi bula rha h tumhe ')

	if msg == "guddu":
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('guddu aapko koi bula rha h')


	if msg == "deepak":
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('deepak ji kaha ho....?')

	if msg == "aurat":
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('Bhawana ji, nasha utaro and aao')

	if msg == "strange":
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('Strange, someone is calling you sir')

	if msg.startswith("search "):
		s = msg[7:100]
		url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/" + s
		response = requests.request("GET", url, headers=sh)
		json_data = json.loads(response.text)
		search = json_data["titles"][0]
		await message.channel.send(search)

	if any(word in msg for word in userdata.sad(1)):
		await message.channel.send(userdata.sad(2))

	if (td == "truth"):
		await message.channel.send(userdata.tad(1))
		time.sleep(5)
		await message.channel.send("Truth or Dare")

	if (td == "dare"):
		await message.channel.send(userdata.tad(2))
		time.sleep(5)
		await message.channel.send("Truth or Dare")

	if (td == "end"):
		await message.channel.send("Game ended")
		game = 0


@tasks.loop(minutes=60)
async def send():
	alarm = client.get_channel(int(os.getenv("RM")))
	await alarm.send("kkrh")
	await alarm.send("****jo bhi ho padhne baitho****")
	await alarm.send("Drink water and stretch a little")


@send.before_loop
async def before():
	await client.wait_until_ready()


send.start()

keep_alive()
client.run(os.getenv("TOKEN"))
