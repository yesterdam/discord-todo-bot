#!/bin/bash

# ✅ 1. ตรวจสอบ .env
if [ ! -f .env ]; then
  echo "⚠️  .env file not found. Please create one with DISCORD_TOKEN=<your-token>"
  exit 1
fi

# ✅ 2. สร้าง backup/ (local volume)
mkdir -p backup

# ✅ 3. สร้าง image
echo "🐳 Building Docker image..."
docker build -t discord-todo-bot .

# ✅ 4. หยุด container เดิมถ้ามี
echo "🛑 Stopping old container (if exists)..."
docker stop todo-bot 2>/dev/null
docker rm todo-bot 2>/dev/null

# ✅ 4.5 เตรียมไฟล์ที่จำเป็นถ้ายังไม่มี
[ ! -f todo.txt ] && touch todo.txt
[ ! -f latest_message.txt ] && touch latest_message.txt

# ✅ 5. รันใหม่
echo "🚀 Running TODO bot..."
docker run -d \
  --name todo-bot \
  --restart always \
  --env-file .env \
  -v "$(pwd)/todo.txt:/app/todo.txt" \
  -v "$(pwd)/latest_message.txt:/app/latest_message.txt" \
  -v "$(pwd)/backup:/app/backup" \
  discord-todo-bot