import discord
from discord.ext import commands
import openai
import spacy
import speech_recognition as sr
from googletrans import Translator
import asyncio
from config import OPENAI_API_KEY
from features.reminders import Reminders
from features.notes import Notes
from features.tasks import Tasks
from features.sentiment_analysis import SentimentAnalysis
from features.weather import WeatherForecast
from features.news import NewsSummary
from features.web_search import WebSearch
from features.image_processing import ImageProcessor
from features.calendar_integration import CalendarIntegration
from features.finance_tracker import FinanceTracker
from cryptography.fernet import Fernet

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
        self.weather = WeatherForecast()
        self.news = NewsSummary()
        self.web_search = WebSearch()
        self.image_processor = ImageProcessor()
        self.calendar = CalendarIntegration()
        self.finance_tracker = FinanceTracker()
        
        # Initialize NLP
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize conversation context
        self.conversation_context = {}
        
        # Initialize adaptive personality
        self.personality = {}
        
        # Initialize translator
        self.translator = Translator()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize encryption
        self.cipher_suite = Fernet(Fernet.generate_key())

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        
    async def on_message(self, message):
        if message.author == self.user:
            return

        try:
            # Process image if attached
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        description = await self.image_processor.describe_image(attachment.url)
                        await message.channel.send(f"I see: {description}")

            # Detect language
            detected_lang = self.translator.detect(message.content).lang
            
            # Translate if not in English
            if detected_lang != 'en':
                translated = self.translator.translate(message.content, dest='en')
                content = translated.text
            else:
                content = message.content
            
            # Perform sentiment analysis
            sentiment = self.sentiment_analysis.analyze(content)
            
            # Process commands
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)
                return
            
            # If not a command, try to understand and respond
            intent = self.recognize_intent(content)
            response = await self.generate_response(message.author.id, content, sentiment, intent)
            
            # Translate response back if necessary
            if detected_lang != 'en':
                response = self.translator.translate(response, dest=detected_lang).text
            
            await message.channel.send(response)
            
            # Update adaptive personality
            self.update_personality(message.author.id, sentiment, intent)
        except Exception as e:
            print(f"Error processing message: {e}")
            await message.channel.send("I'm sorry, I encountered an error while processing your message.")

    def recognize_intent(self, message):
        doc = self.nlp(message)
        # Implement intent recognition logic here
        # For simplicity, we'll just return the root verb of the sentence
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return token.lemma_
        return "unknown"

    async def generate_response(self, user_id, user_message, sentiment, intent):
        try:
            context = self.get_conversation_context(user_id)
            personality = self.get_personality(user_id)
            calendar_events = await self.calendar.list_events(user_id)
            finance_summary = self.finance_tracker.get_summary(user_id)
            prompt = f"User: {user_message}\nSentiment: {sentiment}\nIntent: {intent}\nContext: {context}\nPersonality: {personality}\nCalendar: {calendar_events}\nFinance: {finance_summary}\nAssistant:"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful AI assistant with the following personality traits: {personality}. You have access to the user's calendar and financial information."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            ai_response = response.choices[0].message['content'].strip()
            self.update_conversation_context(user_id, user_message, ai_response)
            return ai_response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble generating a response right now."

    def get_personality(self, user_id):
        return self.personality.get(user_id, "helpful and friendly")

    def update_personality(self, user_id, sentiment, intent):
        if user_id not in self.personality:
            self.personality[user_id] = "helpful and friendly"
        
        if sentiment == "positive":
            self.personality[user_id] += ", more enthusiastic"
        elif sentiment == "negative":
            self.personality[user_id] += ", more empathetic"
        
        if "question" in intent:
            self.personality[user_id] += ", more informative"
        elif "command" in intent:
            self.personality[user_id] += ", more directive"
        
        # Limit personality traits to last 5
        self.personality[user_id] = ", ".join(self.personality[user_id].split(", ")[-5:])

    def get_conversation_context(self, user_id):
        return self.conversation_context.get(user_id, "")

    def update_conversation_context(self, user_id, user_message, ai_response):
        context = f"User: {user_message}\nAssistant: {ai_response}\n"
        if user_id in self.conversation_context:
            self.conversation_context[user_id] += context
        else:
            self.conversation_context[user_id] = context
        # Limit context to last 5 exchanges
        self.conversation_context[user_id] = "\n".join(self.conversation_context[user_id].split("\n")[-10:])

    @commands.command(name='remind')
    async def remind_command(self, ctx, time, *, reminder):
        try:
            result = self.reminders.add_reminder(ctx.author.id, time, reminder)
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error setting reminder: {e}")

    @commands.command(name='note')
    async def note_command(self, ctx, *, content):
        try:
            result = self.notes.add_note(ctx.author.id, content)
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error adding note: {e}")

    @commands.command(name='task')
    async def task_command(self, ctx, *, task):
        try:
            result = self.tasks.add_task(ctx.author.id, task)
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error adding task: {e}")

    @commands.command(name='get_reminders')
    async def get_reminders_command(self, ctx):
        try:
            reminders = self.reminders.get_reminders(ctx.author.id)
            await ctx.send(reminders)
        except Exception as e:
            await ctx.send(f"Error getting reminders: {e}")

    @commands.command(name='get_notes')
    async def get_notes_command(self, ctx):
        try:
            notes = self.notes.get_notes(ctx.author.id)
            await ctx.send(notes)
        except Exception as e:
            await ctx.send(f"Error getting notes: {e}")

    @commands.command(name='get_tasks')
    async def get_tasks_command(self, ctx):
        try:
            tasks = self.tasks.get_tasks(ctx.author.id)
            await ctx.send(tasks)
        except Exception as e:
            await ctx.send(f"Error getting tasks: {e}")

    @commands.command(name='weather')
    async def weather_command(self, ctx, *, location):
        try:
            forecast = await self.weather.get_forecast(location)
            await ctx.send(forecast)
        except Exception as e:
            await ctx.send(f"Error getting weather forecast: {e}")

    @commands.command(name='news')
    async def news_command(self, ctx, *, topic="general"):
        try:
            summary = await self.news.get_summary(topic)
            await ctx.send(summary)
        except Exception as e:
            await ctx.send(f"Error getting news summary: {e}")

    @commands.command(name='search')
    async def search_command(self, ctx, *, query):
        try:
            results = await self.web_search.search(query)
            await ctx.send(results)
        except Exception as e:
            await ctx.send(f"Error performing web search: {e}")

    @commands.command(name='calendar')
    async def calendar_command(self, ctx, action, *, details=None):
        try:
            if action == 'add':
                result = await self.calendar.add_event(ctx.author.id, details)
            elif action == 'list':
                result = await self.calendar.list_events(ctx.author.id)
            else:
                result = "Invalid action. Use 'add' or 'list'."
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error with calendar operation: {e}")

    @commands.command(name='finance')
    async def finance_command(self, ctx, action, *, details=None):
        try:
            if action == 'add':
                result = self.finance_tracker.add_transaction(ctx.author.id, details)
            elif action == 'summary':
                result = self.finance_tracker.get_summary(ctx.author.id)
            else:
                result = "Invalid action. Use 'add' or 'summary'."
            await ctx.send(result)
        except Exception as e:
            await ctx.send(f"Error with finance operation: {e}")

    async def proactive_assistance(self):
        while True:
            for user_id, user_data in self.conversation_context.items():
                try:
                    suggestions = await self.generate_proactive_suggestions(user_id, user_data)
                    if suggestions:
                        user = await self.fetch_user(user_id)
                        await user.send(f"Here are some suggestions based on our recent conversations:\n{suggestions}")
                except Exception as e:
                    print(f"Error in proactive assistance for user {user_id}: {e}")
            await asyncio.sleep(3600)  # Check every hour

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

    async def generate_proactive_suggestions(self, user_id, user_data):
        try:
            prompt = f"Based on the following conversation history, generate proactive suggestions for the user:\n\n{user_data}\n\nSuggestions:"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Generate proactive suggestions based on the conversation history."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            suggestions = response.choices[0].message['content'].strip()
            self.learn_from_suggestions(user_id, suggestions)
            return suggestions
        except Exception as e:
            print(f"Error generating proactive suggestions: {e}")
            return ""

    def learn_from_suggestions(self, user_id, suggestions):
        # Implement basic learning logic here
        # For example, you could store frequently suggested topics or actions
        pass

    @commands.command(name='voice')
    async def voice_command(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        try:
            await ctx.send("Listening for 5 seconds...")
            audio_data = await self.record_audio(voice_client, duration=5)
            text = self.speech_to_text(audio_data)
            await ctx.send(f"I heard: {text}")

            # Process the voice command
            response = await self.generate_response(ctx.author.id, text, "neutral", "voice_command")
            await ctx.send(response)
        finally:
            await voice_client.disconnect()

    async def record_audio(self, voice_client, duration):
        # This is a placeholder. You'll need to implement actual audio recording logic
        # using discord.py's voice features.
        pass

    def speech_to_text(self, audio_data):
        try:
            return self.recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Sorry, there was an error processing the audio."