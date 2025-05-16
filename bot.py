import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='/', help_command=None)

TODO_FILE = "todo.txt"

def ensure_file():
    if not os.path.exists(TODO_FILE):
        open(TODO_FILE, "w").close()

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def add(ctx, *, arg):
    ensure_file()
    if ':' not in arg:
        await ctx.send("❌ รูปแบบไม่ถูกต้อง! กรุณาใช้ /add project_key: project_name")
        return
    key, name = [s.strip() for s in arg.split(':', 1)]
    with open(TODO_FILE, "a") as f:
        f.write(f"{key}: {name} [ ]\n")
    await ctx.send(f"✅ เพิ่มโปรเจกต์ `{key}`: `{name}` แล้วครับ")

@bot.command()
async def remove(ctx, *, key):
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
    if found:
        await ctx.send(f"🗑️ ลบโปรเจกต์ `{key}` ออกจาก list แล้วครับ")
    else:
        await ctx.send(f"❌ ไม่พบโปรเจกต์ `{key}` ใน list ครับ")

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
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if line.startswith(f"{key}:") and "[ ]" in line:
            updated.append(line.replace("[ ]", "[x]", 1))
            found = True
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    if found:
        await ctx.send(f"🎉 ทำเครื่องหมาย `{key}` ว่าเสร็จแล้วครับ")
    else:
        await ctx.send(f"❌ ไม่พบโปรเจกต์ `{key}` ที่ยังไม่เสร็จครับ")

@bot.command()
async def rename(ctx, key: str, *, new_name: str):
    ensure_file()
    with open(TODO_FILE, "r") as f:
        lines = f.readlines()
    updated = []
    found = False
    for line in lines:
        if line.startswith(f"{key}:"):
            status = "[x]" if "[x]" in line else "[ ]"
            updated.append(f"{key}: {new_name} {status}\n")
            found = True
        else:
            updated.append(line)
    with open(TODO_FILE, "w") as f:
        f.writelines(updated)
    if found:
        await ctx.send(f"✏️ เปลี่ยนชื่อโปรเจกต์ `{key}` เป็น `{new_name}` แล้วครับ")
    else:
        await ctx.send(f"❌ ไม่พบโปรเจกต์ `{key}` ใน list ครับ")

bot.run(TOKEN)