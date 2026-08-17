import os
import io
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Telegram Editor Bot!\n\n"
        "📸 Mujhe koi image bhejo.\n\n"
        "Main us image ko:\n"
        "🗜️ Compress\n"
        "📏 Resize\n"
        "🔄 JPG/PNG Convert\n"
        "kar sakta hoon.\n\n"
        "Abhi image bhejo 👇"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    await message.reply_text("⏳ Image process ho rahi hai...")

    photo = message.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    image_data = io.BytesIO()
    await file.download_to_memory(image_data)
    image_data.seek(0)

    image = Image.open(image_data)

    # RGB conversion
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize: maximum width/height 1200px
    max_size = 1200
    image.thumbnail((max_size, max_size))

    # Compress
    output = io.BytesIO()
    image.save(
        output,
        format="JPEG",
        quality=70,
        optimize=True
    )

    output.seek(0)

    await message.reply_document(
        document=output,
        filename="edited_image.jpg",
        caption="✅ Image ready!\n🗜️ Compressed & resized."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Please send an image directly.\n\n"
        "Supported formats: JPG, JPEG, PNG"
    )


def main():
    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN missing! Please add BOT_TOKEN "
            "as an environment variable."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.PHOTO, handle_photo)
    )

    app.add_handler(
        MessageHandler(filters.Document.ALL, handle_document)
    )

    print("🤖 Telegram Editor Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
