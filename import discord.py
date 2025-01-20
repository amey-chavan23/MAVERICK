import discord
from discord.ext import commands
import os

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

# Bot setup with ~ as the prefix
PREFIX = "~"
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load cogs (modular feature files)
cogs = [
    "cogs.moderation",
    "cogs.entertainment",
    "cogs.utility",
    "cogs.ai",
    "cogs.leveling",
    "cogs.management",
    "cogs.reaction_roles"
]

for cog in cogs:
    bot.load_extension(cog)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Run the bot
bot.run("MTMzMDg2OTE3NzE5MTM2Njc0Ng.GGbDsv.Rxnj6b9cxCo4mlYV5MbbOcmxtWZSLwVJroyfH0")

import discord
from discord.ext import commands

# Define the emoji to role mapping
reaction_roles = {
    "💻": "Developer",
    "🎮": "Gamer",
    "🔵": "Blue",
    "🔴": "Red",
    "🟣": "Purple",
    "♂️": "Male",
    "♀️": "Female",
}

# This will store the message ID for the self-role message
role_message_id = None

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setup_roles(self, ctx):
        """Create the self-role message with reactions."""
        embed = discord.Embed(
            title="🎭 Choose Your Roles!",
            description=(
                "React to assign yourself a role:\n\n"
                "💻 - Developer\n"
                "🎮 - Gamer\n"
                "🔵 - Favorite Color: Blue\n"
                "🔴 - Favorite Color: Red\n"
                "🟣 - Favorite Color: Purple\n"
                "♂️ - Male\n"
                "♀️ - Female\n"
            ),
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        reactions = ["💻", "🎮", "🔵", "🔴", "🟣", "♂️", "♀️"]
        for emoji in reactions:
            await message.add_reaction(emoji)

        global role_message_id
        role_message_id = message.id
        await ctx.send("Reaction role message setup complete!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Assign roles based on reactions."""
        if payload.message_id == role_message_id:
            guild = self.bot.get_guild(payload.guild_id)
            role_name = reaction_roles.get(payload.emoji.name)  # Get the role name
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.add_roles(role)
                        print(f"Assigned role '{role_name}' to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove roles based on reactions."""
        if payload.message_id == role_message_id:
            guild = self.bot.get_guild(payload.guild_id)
            role_name = reaction_roles.get(payload.emoji.name)  # Get the role name
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member:
                        await member.remove_roles(role)
                        print(f"Removed role '{role_name}' from {member.name}")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))


from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: commands.MemberConverter):
        """Kick a user."""
        await user.kick(reason="Violation of rules")
        await ctx.send(f"{user.name} has been kicked!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: commands.MemberConverter):
        """Ban a user."""
        await user.ban(reason="Violation of rules")
        await ctx.send(f"{user.name} has been banned!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: commands.MemberConverter, *, reason):
        """Warn a user."""
        await ctx.send(f"{user.name} has been warned for: {reason}")

def setup(bot):
    bot.add_cog(Moderation(bot))


import discord
from discord.ext import commands
import random

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        """Tell a random joke."""
        jokes = ["Why don't skeletons fight each other? They don't have the guts!",
                 "Why did the chicken join a band? Because it had drumsticks!"]
        await ctx.send(random.choice(jokes))

    @commands.command()
    async def meme(self, ctx):
        """Send a random meme."""
        memes = ["Meme1.jpg", "Meme2.jpg", "Meme3.jpg"]
        await ctx.send(random.choice(memes))

def setup(bot):
    bot.add_cog(Entertainment(bot))

import discord
from discord.ext import commands
import asyncio
import requests

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx, time: int, *, message):
        """Set a reminder."""
        await ctx.send(f"I'll remind you in {time} seconds: {message}")
        await asyncio.sleep(time)
        await ctx.send(f"Reminder: {message}")

    @commands.command()
    async def poll(self, ctx, question, *options):
        """Create a poll."""
        if len(options) < 2:
            await ctx.send("Please provide at least two options!")
            return
        embed = discord.Embed(title=question, description="\n".join([f"{i+1}. {option}" for i, option in enumerate(options)]))
        poll_message = await ctx.send(embed=embed)
        for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await poll_message.add_reaction(emoji)

    @commands.command()
    async def weather(self, ctx, city):
        """Get the current weather in a city."""
        api_key = "YOUR_OPENWEATHER_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            await ctx.send(f"The current temperature in {city} is {temp}°C with {description}.")
        else:
            await ctx.send("City not found!")

def setup(bot):
    bot.add_cog(Utility(bot))


import discord
from discord.ext import commands
import openai

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = "YOUR_OPENAI_API_KEY"

    @commands.command()
    async def chat(self, ctx, *, message):
        """AI Chatbot."""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=100
        )
        await ctx.send(response.choices[0].text.strip())

def setup(bot):
    bot.add_cog(AI(bot))


import discord
from discord.ext import commands
import json

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_xp_data()

    def load_xp_data(self):
        try:
            with open("data/leveling.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_xp_data(self):
        with open("data/leveling.json", "w") as f:
            json.dump(self.xp_data, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0, "level": 1}

        self.xp_data[user_id]["xp"] += 10
        if self.xp_data[user_id]["xp"] >= 100:
            self.xp_data[user_id]["xp"] = 0
            self.xp_data[user_id]["level"] += 1
            await message.channel.send(f"{message.author.mention} leveled up to level {self.xp_data[user_id]['level']}!")

        self.save_xp_data()

    @commands.command()
    async def level(self, ctx, user: discord.Member = None):
        """Check your or someone else's level."""
        user = user or ctx.author
        user_id = str(user.id)
        level = self.xp_data.get(user_id, {"level": 1})["level"]
        await ctx.send(f"{user.name} is level {level}.")

def setup(bot):
    bot.add_cog(Leveling(bot))


import discord
from discord.ext import commands
import requests

class ExternalAPIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def github(self, ctx, user):
        """Fetch GitHub user info."""
        url = f"https://api.github.com/users/{user}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title=f"{data['login']}'s GitHub", description=data['bio'], color=discord.Color.blue())
            embed.add_field(name="Public Repos", value=data['public_repos'])
            embed.add_field(name="Followers", value=data['followers'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("GitHub user not found.")

def setup(bot):
    bot.add_cog(ExternalAPIs(bot))




