import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', help_command=None, intents=intents)

TODO_FILE = "todo.txt"
LATEST_MESSAGE_FILE = "latest_message.txt"


def ensure_file():
    if not os.path.exists(TODO_FILE):
        open(TODO_FILE, "w").close()


async def update_list_message(ctx):
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()

    total = len(lines)
    done_count = sum(1 for line in lines if "[x]" in line)

    content = f">>> **TODO list ({done_count}/{total} complete)**\n```txt\n"
    for i, line in enumerate(lines, 1):
        content += f"{i}. {line}"
    content += f"```"
    timestamp = datetime.now().strftime("%A at %I:%M %p")
    content += f"\n{timestamp}"

    try:
        if os.path.exists(LATEST_MESSAGE_FILE):
            with open(LATEST_MESSAGE_FILE, "r") as f:
                msg_id = int(f.read().strip())
            message = await ctx.channel.fetch_message(msg_id)
            await message.edit(content=content)
        else:
            message = await ctx.send(content)
            with open(LATEST_MESSAGE_FILE, "w") as f:
                f.write(str(message.id))
    except Exception:
        message = await ctx.send(content)
        with open(LATEST_MESSAGE_FILE, "w") as f:
            f.write(str(message.id))


@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')


@bot.command()
async def add(ctx, *, arg):
    await ctx.message.delete()
    ensure_file()
    if ':' not in arg:
        await ctx.send("❌ รูปแบบไม่ถูกต้อง! กรุณาใช้ /add project_key: project_name")
        return
    key, name = [s.strip() for s in arg.split(':', 1)]
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if f"{key}:" in line:
            status = "[x]" if "[x]" in line else "[ ]"
            updated.append(f"{status} {key}: {name}\n")
            found = True
        else:
            updated.append(line)
    if not found:
        updated.append(f"[ ] {key}: {name}\n")
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)


@bot.command()
async def remove(ctx, *, key):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if not line.startswith(f"{key}:"):
            updated.append(line)
        else:
            found = True
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)


@bot.command()
async def list(ctx):
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    if not lines:
        await ctx.send("📂 ยังไม่มีโปรเจกต์ใน list เลยครับ")
    else:
        await ctx.send("📋 **รายการโปรเจกต์**\n" + "".join(lines))


@bot.command()
async def done(ctx, *, key):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if f"{key}:" in line and "[ ]" in line:
            updated.append(line.replace("[ ]", "[x]", 1))
            found = True
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)


@bot.command()
async def rename(ctx, key: str, *, new_name: str):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if f"{key}:" in line:
            status = "[x]" if "[x]" in line else "[ ]"
            updated.append(f"{key}: {new_name} {status}\n")
            found = True
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)


bot.run(TOKEN)
