import discord
import google.generativeai as genai
import os

# Configure Google Generative AI
genai.configure(api_key=os.environ["Google_api"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Retrieve the Discord bot token
token = os.getenv('DISCORD_KEY')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # print(f'Message from {message.author}: {message.content}')

        # Check if the bot is mentioned
        if self.user in message.mentions:
            channel = message.channel
            try:
                content = message.content.replace(f'<@{self.user.id}>', '').strip()

                if content:  # Only respond if there's content after the mention
                    response = model.generate_content(content)
                    message_to_send = response.text.strip()
                    await channel.send(message_to_send)
                else:
                    await channel.send("What do you want to know?")
            except Exception as e:
                print(f'Error generating response: {e}')
                await channel.send("Sorry, I couldn't process that.")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
