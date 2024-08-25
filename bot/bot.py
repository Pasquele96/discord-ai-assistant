import discord
from discord.ext import commands
import openai
from config import OPENAI_API_KEY
from features.reminders import Reminders
from features.notes import Notes
from features.tasks import Tasks
from features.sentiment_analysis import SentimentAnalysis

class AIAssistantBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.openai_api_key = OPENAI_API_KEY
        openai.api_key = self.openai_api_key
        
        # Initialize features
        self.reminders = Reminders()
        self.notes = Notes()
        self.tasks = Tasks()
        self.sentiment_analysis = SentimentAnalysis()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        
    async def on_message(self, message):
        if message.author == self.user:
            return

        # Perform sentiment analysis
        sentiment = self.sentiment_analysis.analyze(message.content)
        
        # Process commands
        await self.process_commands(message)
        
        # If not a command, try to understand and respond
        if not message.content.startswith(self.command_prefix):
            response = await self.generate_response(message.content, sentiment)
            await message.channel.send(response)

    async def generate_response(self, user_message, sentiment):
        prompt = f"User message: {user_message}\nSentiment: {sentiment}\nAssistant:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    @commands.command(name='remind')
    async def remind_command(self, ctx, time, *, reminder):
        result = self.reminders.add_reminder(ctx.author.id, time, reminder)
        await ctx.send(result)

    @commands.command(name='note')
    async def note_command(self, ctx, *, content):
        result = self.notes.add_note(ctx.author.id, content)
        await ctx.send(result)

    @commands.command(name='task')
    async def task_command(self, ctx, *, task):
        result = self.tasks.add_task(ctx.author.id, task)
        await ctx.send(result)

    # Add more commands for other features here