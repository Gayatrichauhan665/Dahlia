import discord
import os
import requests
import json
from replit import db
import userdata
import help
import time
from discord.ext import tasks
from keep_alive import keep_alive
client = discord.Client()

jh = {
    'x-rapidapi-key': "3e3b3b108amsh634f6f74abdac28p1b33a3jsndbe9079f48eb",
    'x-rapidapi-host': "jokeapi.p.rapidapi.com"
}

imdbh = {
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

	word = message.content.lower()

	if word == "t&d":
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

	if msg == "pls help":
		await message.channel.send(help.commands())

	if msg == "inspire":
		quote = get_quote()
		await message.channel.send(quote)

	if msg == "joke":
		await message.channel.send(get_joke())

	if msg == "strange":
		"await message.channel.send(file=discord.File('images/wait.jpg'))"
		channel = client.get_channel(int(os.getenv("NT")))
		await channel.send('Someone is calling you sir')


	if msg.startswith("imdb "):
		s = msg[5:100]
		url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/" + s
		response = requests.request("GET", url, headers=imdbh)
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


@tasks.loop(minutes=120)
async def send():
	alarm = client.get_channel(int(os.getenv("RM")))
	await alarm.send("Don't waste time")

@send.before_loop
async def before():
	await client.wait_until_ready()


send.start()

keep_alive()
client.run(os.getenv("TOKEN"))
