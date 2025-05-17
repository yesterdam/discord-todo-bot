import os
import shutil
from datetime import datetime, timezone, timedelta

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

from discord.ext import commands

class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_text = (
            ">>> **TODO Bot Commands**\n\n"
            "`/add <key>: <name>` - เพิ่มหรือแก้ไขโปรเจกต์\n"
            "`/done <key>` - ทำเครื่องหมายว่าเสร็จแล้ว\n"
            "`/pending <key>` - กำลังดำเนินการ\n"
            "`/reject <key>` - กลับไปยังสถานะเริ่มต้น\n"
            "`/remove <key>` - ลบโปรเจกต์ออก\n"
            "`/rename <key> <name>` - เปลี่ยนชื่อโปรเจกต์\n"
            "`/list` - แสดงรายการทั้งหมด\n"
            "`/todo` - เริ่ม todo ใหม่ (ย้ายข้อมูลเก่าไป backup)\n"
        )
        await self.get_destination().send(help_text)

bot = commands.Bot(command_prefix='/', intents=intents, help_command=MyHelpCommand())

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

    content = f">>> **TODO list ({done_count}/{total} complete)**\n"
    content += "[ ] = not started, [-] = in progress, [x] = done\n"
    content += "```txt\n"
    for i, line in enumerate(lines, 1):
        content += f"{i}. {line}"
    content += f"```"
    timestamp = (datetime.now(timezone(timedelta(hours=7)))).strftime("%A at %I:%M %p")
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
    for line in lines:
        if f"{key}:" not in line:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)


@bot.command()
async def list(ctx):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    if not lines:
        await ctx.send("📂 ยังไม่มีโปรเจกต์ใน list เลยครับ")
    else:
        if os.path.exists(LATEST_MESSAGE_FILE):
            try:
                with open(LATEST_MESSAGE_FILE, "r") as f:
                    msg_id = int(f.read().strip())
                old_msg = await ctx.channel.fetch_message(msg_id)
                await old_msg.delete()
            except discord.NotFound:
                pass
            # Instead of removing the file, write empty message_id to avoid file lock issues
            with open(LATEST_MESSAGE_FILE, "w") as f:
                f.write("")
        await update_list_message(ctx)


@bot.command()
async def done(ctx, *, key):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    for line in lines:
        if f"{key}:" in line and "[x]" not in line:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                clean_part = parts[1].split(" (by")[0].strip()
                updated.append(f"[x] {key}: {clean_part} (by {ctx.author.display_name})\n")
            else:
                updated.append(line)
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)

@bot.command()
async def reject(ctx, *, key):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    for line in lines:
        if f"{key}:" in line and "[ ]" not in line:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                clean_part = parts[1].split(" (by")[0].strip()
                updated.append(f"[ ] {key}: {clean_part}\n")
            else:
                updated.append(line)
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)

@bot.command()
async def pending(ctx, *, key):
    await ctx.message.delete()
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    for line in lines:
        if f"{key}:" in line and "[x]" not in line and "[ ]" in line:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                updated.append(f"[-] {key}: {parts[1]} (by {ctx.author.display_name})\n")
            else:
                updated.append(line)
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
    for line in lines:
        if f"{key}:" in line:
            status = "[x]" if "[x]" in line else "[-]" if "[-]" in line else "[ ]"
            updated.append(f"{status} {key}: {new_name}\n")
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    await update_list_message(ctx)

@bot.command()
async def todo(ctx):
    await ctx.message.delete()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)

    if os.path.exists(TODO_FILE):
        todo_backup = os.path.join(backup_dir, f"todo_{timestamp}.txt")
        shutil.copy2(TODO_FILE, todo_backup)
        with open(TODO_FILE, "w") as f:
            f.write("")
    if os.path.exists(LATEST_MESSAGE_FILE):
        msg_backup = os.path.join(backup_dir, f"latest_message_{timestamp}.txt")
        shutil.copy2(LATEST_MESSAGE_FILE, msg_backup)
        with open(LATEST_MESSAGE_FILE, "w") as f:
            f.write("")

    await ctx.send("🆕 เริ่ม TODO list ใหม่เรียบร้อยแล้วครับ (ย้ายข้อมูลเดิมไปที่โฟลเดอร์ backup)")

bot.run(TOKEN)
