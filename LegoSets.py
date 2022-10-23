from random import randint
from discord.ext import commands
from discord import app_commands 
import discord

from bs4 import BeautifulSoup as bs
import requests
import lxml

bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())


@bot.hybrid_command(name = "set", description = "find a lego technic set")
@app_commands.describe(set = 'id of lego tehnic set')
async def set(ctx, set: int):
   url = "https://rebrickable.com/sets/" + str(set) + "-1"
   res = requests.get(url)
   soup = bs(res.text, "lxml")

   error = soup.find("div", id = "content")
   error = error.find("strong")
   if error == None:
      

      table = soup.find("table", class_ = "table table-wrap")
      name = table.find_all("td")[1].text
      inventory = table.find_all("a")[1].text

      img = soup.find("img", class_ = "img-responsive").get("src")

      section = soup.find_all("section", class_ = "padding-xxs")[1]
      sale = section.find_all("span", class_ = "trunc")
      sale = [i.text for i in sale]
      try: section.strike.decompose()
      except: pass
      price = section.find_all("a", target = "_blank")
      price = [price[i].text.replace("\n", "") for i in range(1, len(price), 2)]

      emb = discord.Embed(title = f"{name} : {set}", colour = 11110385, url = url)

      emb.set_image(url = img)
      emb.set_author(name = "Rebrickable", url = "https://rebrickable.com/", icon_url = "https://rebrickable.com/static/img/robo3b.png")
      emb.add_field(name = "Inventory", value = inventory, inline = False)
      if len(sale) > 0:
         for i in range(len(sale)):
            emb.add_field(name = sale[i], value = price[i], inline = True)

      await ctx.send(embed = emb)
   else:
      emb = discord.Embed(title = "Range of lego sets.", url = "https://rebrickable.com/sets/", colour = 11110385)
      emb.set_author(name = "Not Found.")
      await ctx.send(embed = emb, ephemeral = True)


@bot.hybrid_command(name = "cl", description = "command list")
async def cl(ctx):
   emb = discord.Embed(title = "Command list", description = ".set - Find a set of lego technic. Example of using the command: (.set 42111).\n.about - About the author of this bot.\n.cl - Command list.", colour = 11110385)
   
   await ctx.send(embed = emb, ephemeral = True)


@bot.hybrid_command(name = "about", description = "about autor")
async def about(ctx):
   emb = discord.Embed(colour = 11110385)

   emb.set_author(name = "My youtube channel: Andy Iocks LEGO TECHNIC", icon_url = "https://media.discordapp.net/attachments/614738652194406404/938096499248746526/20220131_134113.jpg?width=416&height=416", url = "https://www.youtube.com/channel/UC_wZQU_V0jOb2nwL3YK3G1w")
   await ctx.send(embed = emb, ephemeral = True)

bot.run('TOKEN')
