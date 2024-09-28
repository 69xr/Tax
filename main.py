import discord
from discord.ext import commands
from discord.ui import Button, View
import traceback
from simple_chalk import chalk

CHANNEL_ID = 1229984044561989704  # Replace with your actual channel ID

# Bot intents and initialization
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Define the specific channel ID
CHANNEL_ID = 1229984044561989704  # Replace with your actual channel ID

# Event: Bot is ready
@bot.event
async def on_ready():
    print(chalk.red('Coded By mOoN (69xr)'))
    print(chalk.green("[+] Bot is ready"))
    print(chalk.yellow(f"[+] Bot Shard Count: {bot.shard_count}"))
    print(chalk.magenta(f"[+] Bot User: {bot.user}"))
    print(f"[+] Bot Shard ID: {bot.shard_id}")
    print()
    for guild in bot.guilds:
        print(f"[-] Guild ID: {guild.id}")
        print(f"[-] Guild Name: {guild.name}")
        print(f"[-] Member Count: {guild.member_count}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="mOoN"))

# Ping command to check latency
@bot.command()
async def ping(ctx):
    response_message = f"Ping: {round(bot.latency * 1000)}ms ⏱️"
    await ctx.send(response_message)

# Function to process number
def process_number(input_str):
    input_str = input_str.lower()
    number = 0

    # Handle 'k' for thousands
    if 'k' in input_str:
        number = float(input_str.replace('k', '')) * 1_000
    # Handle 'm' for millions
    elif 'm' in input_str:
        number = float(input_str.replace('m', '')) * 1_000_000
    # Handle regular numbers
    else:
        number = int(input_str)

    # Multiply the number by 1.052632
    result = number * 1.052632
    return int(result)  # Return as integer

# Button that multiplies the result by 2.11
class MultiplyButton(Button):
    def __init__(self, initial_value):
        super().__init__(label="وسيط", style=discord.ButtonStyle.primary)
        self.value = initial_value

    async def callback(self, interaction: discord.Interaction):
        # Multiply the stored value by 2.11 when the button is clicked
        self.value *= 2.11
        # Disable the button after it's clicked
        self.disabled = True
        # Update the message with the new result and disable the button
        await interaction.response.edit_message(content=f" {int(self.value)}", view=self.view)

# Create a view for the button
class MultiplyView(View):
    def __init__(self, initial_value):
        super().__init__()
        # Add a button to the view
        self.add_item(MultiplyButton(initial_value))

# Event: When a message is sent to any text channel
@bot.event
async def on_message(message):
    # Avoid replying to the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message was sent in the specific channel
    if message.channel.id == CHANNEL_ID:
        try:
            # Try processing the number in the message
            result = process_number(message.content)
            
            # Send the result along with the button
            view = MultiplyView(result)
            await message.channel.send(f"{result}", view=view)
            
        except ValueError:
            # Ignore invalid inputs that aren't valid numbers
            pass
        except Exception as e:
            # Catch and log any other unexpected errors
            traceback.print_exc()


bot.run('')
