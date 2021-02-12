import discord
import os
import requests
import json
import random
from replit import db
import userdata
import time
from keep_alive import keep_alive
client = discord.Client()

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "bc", "fuck", "wtf",
    "pgl", "nalayak", "damn it", "wth", "chutiya", "idiot", "stupid"
]

starter_encouragements = [
    "There There", "U Want..??", "chup ho jao!..koi sun lega!",
    "Ok ,I get it why joey wanted to rip off his arm so that he has something to throw!!",
    "ghusse mein fatt mt jana bs :|", "ye kaha fasa diya mujhe:(",
    "kitne bigad gye ho yr tum..itni gaaliya!", "you're awesome",
    "hail Gayatri", "don't worry",
    "soft kitty warm kitty little ball of fur..happy kitty sleepy kitty..pur pur pur..",
    "wanna have some coffee?..", "why are u so damn hairaan honey?",
    "ohh just stop being a cry baby!", "lets watch tbbt",
    "damn it u r cute,be sad!", "don't be sad,kaddu is mad",
    "dont worry divya will dance", "you're the best", "ufffo!!..bs karo!",
    "lets have pizza!", "ok even I am sad now  -_- ", "be a bunny!",
    "ok I m gng to sleep,u feel free to bother me.."
]



jh = {
    'x-rapidapi-key': "07e4f878fdmsh8a653e7caf8b089p1587afjsneb326fd7f412",
    'x-rapidapi-host': "joke3.p.rapidapi.com"
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
	                            "https://joke3.p.rapidapi.com/v1/joke",
	                            headers=jh,
	                            params={"nsfw": "true"})
	json_data = json.loads(response.text)
	joke = json_data["content"]
	return (joke)


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

	if msg=="guddu":
		await message.channel.send(file=discord.File('images/guddu.JPG'))
  

	if msg.startswith("search "):
		s = msg[7:100]
		url = "https://imdb-internet-movie-database-unofficial.p.rapidapi.com/search/" + s
		response = requests.request("GET", url, headers=sh)
		json_data = json.loads(response.text)
		search = json_data["titles"][0]
		await message.channel.send(search)

	if any(word in msg for word in sad_words):
		await message.channel.send(random.choice(starter_encouragements))

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


keep_alive()
client.run(os.getenv("TOKEN"))
