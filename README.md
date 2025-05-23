# discord-todo-bot
A simple Discord bot for managing a shared TODO list within your team. Easily track tasks, mark them as done, and keep everyone in sync — all from your Discord server.

## 📌 How to Use

This bot helps your team manage a shared TODO list directly in Discord using simple commands.

### ✅ Commands Overview

#### `/add <key>: <project name>`
Add or rename a project to the TODO list using a short key and full project name.

**Example:**
```
/add project1: com-example-vision-ocr
```
---
#### `/list`
Show all projects in the TODO list with their current status. This command also resets the displayed message for a clean refresh.

---
#### `/done <key>`
Mark the project as completed. The bot will update the status to `[x]` and record the user who completed it.

**Example:**
```
/done project1
```

---
#### `/pending <key>`
Mark the project as in progress. The bot will update the status to `[-]` and note the user responsible.

**Example:**
```
/pending project1
```

---
#### `/reject <key>`
Revert the project status back to `[ ]` and remove any user attribution.

**Example:**
```
/reject project1
```

---
#### `/remove <key>`
Remove a project from the list.

**Example:**
```
/remove project1
```

---
#### `/rename <key> <new project name>`
Rename the full project name while keeping the key the same.

**Example:**
```
/rename project1 com-example-new-ocr
```

---
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

### 🐳 Docker Build & Run

You can run the bot using Docker:

#### 🔨 Build the image
```bash
docker build -t discord-todo-bot .
```

#### 🚀 Run the container
```bash
docker run --rm -e DISCORD_TOKEN=your_token_here discord-todo-bot
```

- Replace `your_token_here` with your actual bot token.
- To persist data, you can mount a volume:
```bash
docker run --rm -e DISCORD_TOKEN=your_token_here -v $(pwd)/todo.txt:/app/todo.txt discord-todo-bot
```