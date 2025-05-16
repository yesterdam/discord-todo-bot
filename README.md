# discord-todo-bot
A simple Discord bot for managing a shared TODO list within your team. Easily track tasks, mark them as done, and keep everyone in sync — all from your Discord server.

## 📌 How to Use

This bot helps your team manage a shared TODO list directly in Discord using simple commands.

### ✅ Commands

#### `/add <key>: <project name>`
Add a new project to the TODO list using a short key and full project name.

**Example:**
```
/add project1: com-example-vision-ocr
```

#### `/list`
Show all projects in the TODO list with their current status.

#### `/done <key>`
Mark the project as completed.

**Example:**
```
/done project1
```

#### `/remove <key>`
Remove a project from the list.

**Example:**
```
/remove project1
```

#### `/rename <key> <new project name>`
Rename the full project name while keeping the key the same.

**Example:**
```
/rename project1 com-example-new-ocr
```

### 🗂 Data Storage
All tasks are stored in a simple `todo.txt` file with the format:
```
TODO list (1/5 complete)

1. [ ] project1: alpha-api
2. [x] project2: beta-dashboard
3. [ ] project3: gamma-core
4. [ ] project4: delta-auth
5. [ ] project5: epsilon-service

Friday at 12:19 PM
```

### 🔐 Bot Token
Make sure to store your Discord Bot Token in a `.env` file:
```
DISCORD_TOKEN=your_token_here
```

Do not commit this file to version control.

### Invite
[Invite the bot to your server](https://discord.com/oauth2/authorize?client_id=1372778050730725446&scope=bot&permissions=75776)

> Note: After inviting the bot, you will only see it online in your Discord server **if the bot program is currently running** (e.g., via `python bot.py`).
