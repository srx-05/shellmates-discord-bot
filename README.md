# 🤖 Shellmates Discord Bot

A feature-rich Discord bot built with Python and discord.py for community management, moderation, and engagement.

## 🚀 Features

### 🛡️ Moderation
- **Banned Words System**: Automatically detect and delete messages containing banned words
- **Role-based Permissions**: Restrict commands to Admin/Mod roles
- **Auto Message Filtering**: Real-time message monitoring and filtering

### 🎯 Events & Reminders
- **Event Management**: Create, list, and manage community events
- **Smart Reminders**: Automatic DM reminders for upcoming events
- **Customizable Timing**: Set reminders for any time before events

### ❓ Interactive Quiz System
- **Multiple Difficulties**: Easy, medium, and hard quiz questions
- **Points & Leaderboard**: Earn points and compete on the leaderboard
- **Cyber Security Focus**: Educational content about cyber security

### 📚 Cyber Facts
- **Knowledge Database**: Share and store interesting cyber security facts
- **Categorized Content**: Organized fact repository

### 🛠️ Command Management
- **Usage Tracking**: Monitor command popularity and usage
- **Dynamic Help System**: Contextual help commands
- **Command Database**: Manage and update command descriptions dynamically
- **Error Handling**: Robust error handling and user feedback

## 🎮 Available Commands
### 👥 For All Users
- **/quiz [difficulty]** - Take a cyber security quiz

- **/leaderboard** - View quiz points leaderboard

- **/events** - List upcoming events

- **/past_events** - Show past events

- **/remind_me <event_id> [minutes]** - Get reminders for events

- **/my_reminders** - View your active reminders

- **/reminder_status** - Check reminder service status

### 🛡️ For Admin/Mod Only
- **/banword <word>** - Add word to banned list

- **/unbanword <word>** - Remove word from banned list

- **/listbanned** - Show all banned words

-  **/add_event <title> <date> <time> <description>** - Create new event

-  **/remove_event <id/title>** - Delete an event

-  **/start_reminders** - Start reminder service

-  **/stop_reminders** - Stop reminder service

-  **/cleanup_reminders** - Clean up expired reminders
  
-  **/add_command <name> [category] <description>** - Add new command to database

-  **/update_command <name> <description>** - Update command description

 - **/delete_command <name>** - Delete command from database

## 🏗️ Project Structure
```
shellmates-discord-bot/
├── bot/
│ ├── cogs/
│ │ ├── banned_words.py 
│ │ ├── cyberfacts_commands.py 
│ │ ├── events_commands.py 
│ │ ├── event_reminder.py 
│ │ ├── quiz_commands.py 
│ │ ├── command_management.py =
│ │ ├── help_commands.py =
│ │ └── error_handler.py 
│ └── bot.py # Main bot class
├── database/
│ ├── Repositories/
│ │ ├── bannedwordRepo.py 
│ │ ├── cyberfactsRepo.py 
│ │ ├── eventRepo.py 
│ │ ├── EventReminderRepo.py 
│ │ ├── quizRepo.py
│ │ └── userRepo.py 
│ ├── connection.py 
│ └── init.py
├── config.py
├── main.py # Application entry point
└── requirements.txt # Python dependencies
```
