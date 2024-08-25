# Discord AI Assistant Bot

This Discord bot is an AI-powered personal assistant with various features to help manage tasks, notes, and reminders. It also includes basic sentiment analysis to adapt its responses to user messages.

## Features

- Reminders with specific dates and times
- Note-taking with organization capabilities
- Task and to-do list management with priorities and due dates
- Basic sentiment analysis of conversations
- Natural language understanding for command processing

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/discord-ai-assistant.git
   cd discord-ai-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your Discord bot token and OpenAI API key:
   ```
   DISCORD_TOKEN=your_discord_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the bot:
   ```
   python main.py
   ```

## Usage

The bot responds to commands prefixed with `!`. Here are some basic commands:

- `!remind [time] [reminder]`: Set a reminder
  Example: `!remind 2023-05-30 14:30 Team meeting`

- `!note [content]`: Add a note
  Example: `!note Remember to buy groceries`

- `!task [task description]`: Add a task
  Example: `!task Finish project report`

- `!tasks`: View your current tasks

- `!notes`: View your notes

- `!reminders`: View your current reminders

The bot will also respond to natural language messages, adapting its tone based on the detected sentiment of the user's message.

## Project Structure

- `main.py`: Entry point for the bot
- `config.py`: Configuration file for environment variables
- `bot/bot.py`: Main bot class with command handling
- `features/`: Directory containing individual feature implementations
  - `reminders.py`: Reminders functionality
  - `notes.py`: Notes functionality
  - `tasks.py`: Tasks functionality
  - `sentiment_analysis.py`: Basic sentiment analysis

## Contributing

Feel free to fork this project and submit pull requests with new features or improvements!

## License

This project is licensed under the MIT License.