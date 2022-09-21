from discord.ext import commands
import discord
import random
import requests

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 257499971194978304  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

### Warm-up 

@bot.command(pass_context=True)
async def name(ctx):
    await ctx.send(ctx.message.author)

@bot.command(pass_context=True)
async def d6(ctx):
    await ctx.send(random.randrange(1,7,1))

@bot.listen()
async def on_message(message):
    if (message.content == "Salut tout le monde"):
        await message.channel.send("Salut tout seul")

### Administration

@bot.command(pass_context=True)
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="adminn")
    if role is None:
        # Doesn't exist, create the role here
        role = await ctx.guild.create_role(name="adminn")
    permissions = discord.Permissions()
    permissions.update(administrator=True)
    await role.edit(permissions= permissions)
    await member.add_roles(role)

@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member):
    reasons="you're ban by the bot!"
    await ctx.guild.ban(member, reason=reasons) # Bans the user.
    await ctx.send(f"{member} has been successfully banned.") # messages channel to tell everyone it worked

@bot.command(pass_context=True)
async def count(ctx):
    online_members = []
    offline_members = []
    idle_members = []
    doNotDisturb_members = []
    for member in ctx.guild.members:
        if member.status is discord.Status.online:
            online_members.append(member.name)
        elif member.status is discord.Status.offline:
            offline_members.append(member.name)
        elif member.status is discord.Status.idle:
            idle_members.append(member.name)
        elif member.status is discord.Status.dnd:
            doNotDisturb_members.append(member.name)
    
    online = ""
    offline = ""
    idle = ""
    dnd = ""
    if len(online_members) > 0:
        for m in online_members:
            online += m + ",  "
        online += " are online.  "
    if len(offline_members) > 0:
        for m in offline_members:
            offline += m + ",  "
        offline += " are offline.  "
    if len(idle_members) > 0:
        for m in idle_members:
            idle += m + ",  "
        idle += " are idle.  "
    if len(doNotDisturb_members) > 0:
        for m in doNotDisturb_members:
            dnd += m + ",  "
        dnd += " are dnd."

    await ctx.send(online + offline + idle + dnd)

### It's all fun and games

@bot.command(pass_context=True)
async def xkcd(ctx):
    response = requests.get("https://c.xkcd.com/random/comic/")
    await ctx.send(response.url)

@bot.command(pass_context=True)
async def poll(ctx, question: str):
    allowed_mentions = discord.AllowedMentions.all()
    await ctx.send(content = "@here " + question, allowed_mentions = allowed_mentions)
    
    message = await ctx.send(question)
    await message.add_reaction("\N{THUMBS UP SIGN}")
    await message.add_reaction("\N{THUMBS DOWN SIGN}")

token = "<Your discord bot token>"
bot.run(token)  # Starts the bot