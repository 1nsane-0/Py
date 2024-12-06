    for chat_id in user_progress:
        current_index = user_progress[chat_id]

        if current_index < len(sections) - 1:
            # Объединяем текущую строку и следующую
            header = sections[current_index].strip()
            content = sections[current_index + 1].strip()
            full_message = f"{header}\n\n{content}"

            # Отправляем объединённое сообщение
            await bot.send_message(chat_id=int(chat_id), text=full_message)

            # Обновляем прогресс
            user_progress[chat_id] += 2  # Переходим сразу на 2 строки вперёд
            save_user_progress(user_progress)
        else:
            await bot.send_message(chat_id=int(chat_id), text="Все части текста уже отправлены!")

# Функция для обнуления прогресса
async def reset_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    user_progress[chat_id] = 0  # Сбрасываем прогресс пользователя
    save_user_progress(user_progress)
    await update.message.reply_text("Ваш прогресс был успешно обнулён!")

# Основной блок
if __name__ == "__main__":
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Планировщик задач
    scheduler = AsyncIOScheduler(timezone="Europe/Berlin")

    # Добавление задачи в планировщик
    scheduler.add_job(send_daily_message, trigger="cron", hour=12, minute=0)
    scheduler.start()

    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Получить следующую часть"), send_next_part))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Обнулить прогресс"), reset_progress))

    # Запуск бота
    print("Бот запущен. Отправьте команду /start, чтобы подписаться.")
    application.run_polling()
