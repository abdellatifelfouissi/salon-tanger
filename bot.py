import telebot, json, requests, base64, os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PHONE = "0610845988"

bot = telebot.TeleBot(BOT_TOKEN)

def update_catalog(title, image_url, type_):
    url = f"https://api.github.com/repos/{REPO}/contents/catalog.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers).json()
    data = json.loads(base64.b64decode(r['content']).decode())
    if not title:
        title = "Salon Nouveau"
    data.append({"title": title, "price": "Sur Mesure", "type": type_, "image": image_url})
    new = base64.b64encode(json.dumps(data, indent=2).encode()).decode()
    requests.put(url, headers=headers, json={"message": "Nouveau salon", "content": new, "sha": r['sha']})

@bot.message_handler(content_types=['photo', 'video'])
def handle(message):
    if message.photo:
        fid = message.photo[-1].file_id
        typ = "image"
    else:
        fid = message.video.file_id
        typ = "video"
    info = bot.get_file(fid)
    furl = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{info.file_path}"
    title = message.caption if message.caption else "Salon Nouveau"
    update_catalog(title, furl, typ)
    bot.reply_to(message, f"✅ تزادت فالكتالوغ: {title}")

bot.polling()
