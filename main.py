import os
import asyncio
import discord
from discord.ext import commands
import pandas as pd
import requests
import psxdata

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} - SilaStock is Fully Operational!")

@bot.command(name="buy")
async def buy_signals(ctx):
    await ctx.send("🔍 Scanning PSX market dynamically for high-potential trading signals...")
    
    def fetch_data():
        try:
            # Dynamic query to PSX screener
            df = psxdata.screener()
            if df is None or df.empty:
                return "Unable to retrieve data from PSX at the moment."
            
            # Simple volume/price filters for active stocks
            filtered = df[(df['Volume'] > 100000) & (df['Change'] > 0)]
            top_picks = filtered.sort_values(by='Volume', ascending=False).head(5)
            
            if top_picks.empty:
                return "No high-volume buy signals found in the current session."
            
            response = "**📈 SilaStock PSX Buy Signals:**\n\n"
            for _, row in top_picks.iterrows():
                response += f"• **{row['Symbol']}** | Price: PKR {row['Current']} | Change: +{row['Change']}% | Vol: {row['Volume']:,}\n"
            return response
        except Exception as e:
            return f"Error analyzing PSX data: {str(e)}"

    # Run blocking PSX data pull in a background thread to prevent bot freezing
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, fetch_data)
    await ctx.send(result)

# Retrieve token safely from Render Environment Variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_BOT_TOKEN environment variable not set!")
