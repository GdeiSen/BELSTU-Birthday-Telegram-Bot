import logging
import pathlib
from database import *
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters, ConversationHandler

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

database = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("Регистрация",
                                 callback_data="reg"),
            InlineKeyboardButton("Помощь", callback_data="help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    path = pathlib.Path("assets/7.jpg")
    await update.message.reply_photo(
        photo=open(path, "rb"),
        reply_markup=reply_markup,caption="Мы уже знаем, что ты - талантливый и смелый программист, но у нас есть еще одна интересная тайна, которую мы хотим раскрыть. Сегодня ты находишься в мире, где симметрия играет важную роль - в мире Зазеркалья.\n\nТвоя задача - пройти все наши испытания, отмечаясь в боте. После того, как ты успешно завершишь все задания, мы отправим тебе секретные координаты, по которым ты сможешь получить призы от iTechArt.\n\nЧтобы получить отметку о выполнении задания, просто сообщи нашим организаторам свой уникальный ID, который мы выдадим тебе после регистрации /reg . Отслеживай статус выполнения своих заданий с помощью команды /profile .Если что-то станет непонятно напиши /help мы тебе поможем!\n\nУдачи, и пусть зеркала всегда отражают твои таланты!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(
        "<b>Раздел помощи для игрока</b>\n\n<b>Инструкция</b>\n<b>1. </b>Перед началом использования бота и прохождения конкурсов вам будет необходимо зарегистрироваться. Для этого вам нужно использовать команду /reg или нажать на соответсвующую кнопку 'регистрация' под начальным сообщением бота\n<b>2. </b>После процесса регистрации вам будет присвоен уникальный индентификатор. Его значение можно увидеть в сообщении об успешной регистрации или в сообщении вашего профиля, которое можно просмотреть с помощью команды /profile. Данный номер необходимо показывать администраторам конкурса при успешном прохождении испытания.\n<b>3. </b>Для просмотора вашего прогресса также используется команда /profile. В данном сообщении можно просмотреть статус каждого испытания конкурса\n<b>4. </b>Для того чтобы узнать о каждом испытании более подробно, используйте команду /tasks. При активации данной команды вам будет выведен список кнопок с названиями испытаний. Выберите интерисующее испытание путем нажатия на кнопку\n<b>5. </b>Для сброса вашего прогресса используется команда /reset\n\n<b>Другие моменты:</b>\n<b>1. </b>Из-за нарушений правил ваш аккаунт может быть заблокирован. Однако если вы счиатете что это ошибка, обратитесь к администраторам конкурса\n<b>2. </b>После прохождения всех заданий ваш аккаунт будет отмечен. Не пытайтесь нарушать правила конкурса.\n\n<b>Раздел помощи для администратора</b>\n\n<b>Инструкция:</b>\n<b>1. </b>Перед началом администрирования ознакомьтесь с отдельным приложением для регистрации администраторов\n<b>2. </b>После прохождения этапа регистрации функционал администратора будет отличаться от функционала игрока. Вам также станет доступна команда /manage. С помощью данной команды осуществляются все функции администрации игроков\n<b>3. </b>При успешном прохождении испытанния игроком, необходимо активировать команду /manage и ввести уникальный номер игрока в чат после соответствующего наводящего сообщения. Если такого номера нет в базе данных игроков, то возможно игрок не прошел регистрацию или была допущена ошибка в наборе числа в чат. Затем необходимо выбрать параметр 'отметить' для регистрации успешного прохождения испытания. При активации данного параметра будет выведен статусный список прохождения заданий игрока. Также под данным списком будет выведен список кнопок. При нажатии кнопки с названием испытания будет произведена замена статуса данного испытания у игрока на противоположный от текущего значения.\n<b>4. </b>В случае нарушения правил конкурса будет предоставлена возможность блокировки игрока с помощью режима 'заблокировать' под сообщением вызванным командой /manage. В случае блокировки игрок не сможет просмотреть свой прогресс а также сделать сброс аккаунта.\n<b>5. </b>Для того чтобы просмотреть информацию об игроке выберите режим 'Прогресс'\n<b>6. </b>В случае прохождении игроком всех испытаний и получении приза, необходимо обозначить аккаунт игрока с помощью режима 'Завершить'. В случае не полном прохождении испытаний, действие будет отклонено.При повторной активации данного режима, статус будет изменен на противоположный.", parse_mode="HTML")


async def reg_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if await database.get_user(user.id):
        await update.effective_chat.send_message(
            f"⚠️ <b>Ты уже зарегистрирован!</b>\n\nЕсли ты хочешь сбросить свой прогресс, то введи команду /reset", parse_mode="HTML"
        )
    else:
        if context.args:
            if context.args[0] == "admin":
                await database.add_user(user.id, 0, user.first_name, 1)
                await update.effective_chat.send_message(
                    f"✅ <b>Регистрация успешно завершена!</b>\n\nТеперь ты можешь приступить к администрированию пользователей!\n\nВведи команду /manage для доступа ко всем функциям администрирования\n\nЕсли что-то станет не понятно введи команду /help", parse_mode="HTML")
        else:
            await database.add_user(user.id, 0, user.first_name)
            user = await database.get_user(user.id)
            await update.effective_chat.send_message(
                f"✅ <b>Регистрация успешно завершена!</b>\n\nТеперь ты можешь приступить к выполнению заданий!\n\n<b>Твой индентификатор: {user[0]}</b>\n\nОбязательно изучи каждое задание с помощью команды /tasks\n\nЧтобы просмотреть свой текущий прогресс введи команду /profile\n\nЕсли что-то станет не понятно введи команду /help\n\nНе затеряйся в зазеркалье!", parse_mode="HTML")


async def get_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = await database.get_all_users()
    await update.message.reply_html(
        f"<u>Список пользователей:</u>\n\n" +
        "\n".join(
            [f"{user[0]} - {user[1]} - {user[2]} - {user[3]}" for user in users])
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = await database.get_user(user.id)
    if not db_user:
        await update.effective_chat.send_message(
            f"⚠️ <b>Ты еще не зарегистрирован!</b>\n\nДля регистрации введи команду /reg", parse_mode="HTML"
        )
        return
    if db_user[2] == 1:
        await update.effective_chat.send_message(
            f"⚠️ <b>К сожалению твой аккаунт был исключен для участия в мероприятии!</b>\n\nТы не можешь активировать эту функцию по данной причине\n\nЕсли ты считаешь, что это ошибка, то обратись к администратору", parse_mode="HTML"
        )
        return
    tasks = await database.get_all_tasks()
    outputHTML = f"<b>Профиль пользователя</b> {user.mention_html()}\n\n"
    outputHTML += f"<b>Идентификатор:</b> {db_user[0]}\n"
    if db_user[4] == 1:
        outputHTML += f"👑 <b>Текущий статус: Администратор</b>\n\nХотим тебе напомнить, что ты являешься администратором, поэтому прогресс тебе недоступен\n\n"
        await update.effective_chat.send_message(outputHTML, parse_mode="HTML")
    else:
        counter = 0
        outputHTML += f"📊 <b>Текущий прогресс:</b>\n\n"
        for task in tasks:
            if await database.get_user_task(db_user[0], task[0]):
                outputHTML += f"✅ <b>{task[1]}</b>\n"
                counter += 1
            else:
                outputHTML += f"❌ <b>{task[1]}</b>\n"
            outputHTML += f"{task[2]}\n{task[6]}\n\n"
        if counter == 7:
            outputHTML += f"🎉 <b>Поздравляем! Ты выполнил все задания!</b>\n\nНайди наших людей на 3 этаже.  И покажи свой прогресс в телеграмме. Твоя награда ждет тебя."
        outputHTML += f"Для получения информации о задании введи команду /tasks\n\nЕсли что-то станет не понятно введи команду /help\n\n"
        await update.effective_chat.send_message(outputHTML, parse_mode="HTML")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = await database.get_user(user.id)
    if db_user[2] == 1:
        await update.effective_chat.send_message(
            f"⚠️ <b>К сожалению твой аккаунт был исключен для участия в мероприятии!</b>\n\nТы не можешь активировать эту функцию по данной причине\n\nЕсли ты считаешь, что это ошибка, то обратись к администратору", parse_mode="HTML"
        )
        return
    if not db_user:
        await update.effective_chat.send_message(
            f"⚠️ <b>Ты еще не зарегистрирован!</b>\n\nДля регистрации введи команду /reg", parse_mode="HTML"
        )
        return
    user_tasks = await database.get_user_tasks(user.id)
    for task in user_tasks:
        await database.delete_user_task(user.id, task[1])
    await database.delete_user(user.id)
    await update.effective_chat.send_message(
        f"✅ <b>Прогресс успешно сброшен!</b>\n\nПеред тем как приступить к выполнению заданий, тебе необходимо снова зарегестрироваться, для этого введи команду /reg", parse_mode="HTML")


async def tasks_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = await database.get_all_tasks()
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.delete_message()
    keyboard = []
    for task in tasks:
        keyboard.append([InlineKeyboardButton(
            task[1], callback_data=f"task_info_{task[0]}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_chat.send_message(
        f"<b>Выбери задание, чтобы получить информацию о нем</b>\n\nЕсли что-то написано непонятно введи команду /help и мы тебе обязательно поможем",
        reply_markup=reply_markup, parse_mode="HTML"
    )


async def manage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = await database.get_user(user.id)
    if not db_user:
        keyboard = [
            [InlineKeyboardButton(
                "Регистрация", callback_data="reg")]
        ]
        await update.effective_chat.send_message(
            f"⚠️ <b>Ты еще не зарегистрирован!</b>\n\nДля регистрации введи команду /reg", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    if db_user[4] == 0:
        await update.effective_chat.send_message(
            f"⚠️ <b>У тебя нет доступа к этой команде!</b>\n\nНеобходим аккаунт администратора", parse_mode="HTML"
        )
        return
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data="cancel")]
        ]
    await update.effective_chat.send_message(f"<b>Введите индентификатор игрока в чат</b>\n\nВведите системный индентификатор игрока, который он обязан предоставить для регистрации прохождения задания\n\nВ случае возможных проблем введите команду /help для поиска решения их устранения", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return 1


async def select_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.text
    user = await database.get_user_by_id(user_id)
    keyboard = [
        [InlineKeyboardButton("Отмена", callback_data=f"cancel")]
    ]
    if not user:
        await update.effective_chat.send_message(
            f"⚠️ <b>Пользователь с таким индетификатором не найден!</b>\n\nПроверьте правильность введенных данных и повторите ввод еще раз", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 1
    if user[4] == 1:
        await update.effective_chat.send_message(
            f"⚠️ <b>Пользователь является администратором!</b>\n\nПроверьте правильность введенных данных и повторите ввод еще раз", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 1
    keyboard = [
        [InlineKeyboardButton("Отметить", callback_data=f"complete_user_callback_{user_id}")],[InlineKeyboardButton("Заблокировать", callback_data=f"block_user_callback_{user_id}")],[InlineKeyboardButton("Прогресс", callback_data=f"profile_user_callback_{user_id}")],[InlineKeyboardButton("Завершить", callback_data=f"end_user_callback_{user_id}")],[InlineKeyboardButton("Отмена", callback_data=f"cancel")]
    ]
    await update.effective_chat.send_message(
        f"<b>Игрок: {user[3]}</b>\n<b>Системный индетификатор:</b> {user[0]}\n<b>Внешний индентификатор:</b> {user[1]}\nЗаблокирован: {user[2]}\nПолучил приз: {user[5]}\n\nВыберите действие, которое хотите совершить с данными пользователя", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))
    return 2


async def block_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.callback_query.data.split("_")[3]
    user = await database.get_user_by_id(user_id)
    if user[2] == 0:
        await database.block_user(user_id)
        await update.effective_chat.send_message(
            f"✅ <b>Пользователь успешно заблокирован!</b>\n\nДля повторной разблокировки игрока снова воспользуйтесь данной командой\n\nДля повторного редактирования игрока введите /manage", parse_mode="HTML"
        )
    else:
        await database.unblock_user(user_id)
        await update.effective_chat.send_message(
            f"✅ <b>Пользователь успешно разблокирован!</b>\n\nДля повторной блокировки игрока снова воспользуйтесь данной командой\n\nДля повторного редактирования игрока введите /manage", parse_mode="HTML"
        )
    await query.answer("Принято")
    await update.callback_query.message.delete()
    return ConversationHandler.END


async def profile_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.callback_query.data.split("_")[3]
    user = await database.get_user_by_id(user_id)
    tasks = await database.get_all_tasks()
    outputHTML = f"<b>Игрок: {user[3]}</b>\n<b>Системный индетификатор:</b> {user[0]}\n<b>Внешний индентификатор:</b> {user[1]}\nЗаблокирован: {user[2]}\nПолучил приз: {user[5]}\n\n"
    outputHTML += f"<b>Текущий прогресс игрока:</b>\n\n"
    for task in tasks:
        if await database.get_user_task(user_id, task[0]):
            outputHTML += f"✅ <b>{task[1]}</b>\n"
        else:
            outputHTML += f"❌ <b>{task[1]}</b>\n"
    outputHTML += f"\n\nДля повторного редактирования игрока введите /manage"
    await update.effective_chat.send_message(
        outputHTML, parse_mode="HTML"
    )
    await query.answer("Принято")
    await update.callback_query.message.delete()
    return ConversationHandler.END


async def complete_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.callback_query.data.split("_")[3]
    user = await database.get_user_by_id(user_id)
    tasks = await database.get_all_tasks()
    outputHTML = f"<b>Игрок: {user[3]}</b>\n<b>Системный индетификатор:</b> {user[0]}\n<b>Внешний индентификатор:</b> {user[1]}\n\n"
    outputHTML += f"<b>Текущий прогресс игрока:</b>\n\n"
    for task in tasks:
        if await database.get_user_task(user_id, task[0]):
            outputHTML += f"✅ <b>{task[1]}</b>\n"
        else:
            outputHTML += f"❌ <b>{task[1]}</b>\n"
    keyboard = []
    for task in tasks:
        keyboard.append([InlineKeyboardButton(
            task[1], callback_data=f"complete_task_callback_{user_id}_{task[0]}")])
    keyboard.append([InlineKeyboardButton("Отмена", callback_data=f"cancel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    outputHTML += "\n\nВыберите задание, статус которого необходимо изменить на противоположный"
    await update.callback_query.message.edit_text(
        outputHTML, parse_mode="HTML", reply_markup=reply_markup
    )
    await query.answer("Отправлено")
    return 2


async def end_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = await database.get_user_by_id(update.callback_query.data.split("_")[3])
    tasks = await database.get_all_tasks()
    flag = True
    for task in tasks:
        if not await database.get_user_task(user[0], task[0]):
            flag = False
    if user[5] == 1:
        await database.unend_user(user[0])
        await update.callback_query.message.edit_text(
            f"✅ <b>Пользователь не завершил игру!</b>\n\nПользователь был отмечен как 'не получивший приз'\n\nДля повторного редактирования игрока введите /manage", parse_mode="HTML")
    elif flag:
        await database.end_user(user[0])
        await update.callback_query.message.edit_text(
            f"✅ <b>Пользователь успешно завершил игру!</b>\n\nПользователь был отмечен как 'дисквалификацирован' по причине окончания игры\n\nДля повторного редактирования игрока введите /manage", parse_mode="HTML")
    else:
        await update.callback_query.message.edit_text(
            f"❌ <b>Пользователь не может завершить игру!</b>\n\nПользователь не выполнил все задания\n\nДля повторного редактирования игрока введите /manage", parse_mode="HTML")
    await query.answer("Выполнено")
    return ConversationHandler.END
        

async def complete_task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.callback_query.data.split("_")[3]
    task_id = update.callback_query.data.split("_")[4]
    task = await database.get_task(task_id)
    user_task = await database.get_user_task(user_id, task_id)
    if user_task:
        await database.delete_user_task(user_id, task_id)
        await update.callback_query.message.reply_html(
            f"⭕ <b>Задание отмечено как не выполненное</b>\n\n<b>{task[1]}</b> - {task[2]} было удалено из списка выполненных\n\nДля повторного редактирования игрока введите /manage"
        )
    else:
        await database.add_user_task(user_id, task_id, "complete")
        await update.callback_query.message.reply_html(
            f"✅ <b>Задание отмечено как выполненное</b>\n\n<b>{task[1]}</b> - {task[2]} было добавлено в список выполненных\n\nДля повторного редактирования игрока введите /manage"
        )
    await update.callback_query.message.delete()
    await query.answer("Отправлено")
    return ConversationHandler.END


async def task_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    task_id = query.data.split("_")[2]
    task = await database.get_task(task_id)
    keyboard = [
        [
            InlineKeyboardButton("Назад", callback_data=f"tasks"),
        ],
    ]
    path = pathlib.Path("assets/" + task[5])
    await query.message.reply_photo(
        path,
        caption=f"<b>{task[1]}</b>\n\n{task[4]}\n\n<b>{task[6]}</b>", 
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
    )
    await query.message.delete()
    await query.answer("Дело сделано!")


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await update.callback_query.message.reply_html(
        "⚠️ <b>Действие отменено</b>\n\nДля повторного редактирования игрока введите /manage"
    )
    await update.callback_query.message.delete()
    await query.answer("Принято")
    return ConversationHandler.END
 

def main() -> None:
    application = Application.builder().token(
        "6043715700:AAEsI1gMd9RhP6hBMZn4mRumOMHzWNfGiao").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reg", reg_command))
    application.add_handler(CommandHandler("users", get_users_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("tasks", tasks_info_command))
    application.add_handler(CallbackQueryHandler(
        task_info_callback, pattern="task_info_*"))
    application.add_handler(CallbackQueryHandler(reg_command, pattern="reg *"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="help"))
    application.add_handler(CallbackQueryHandler(tasks_info_command, pattern="tasks"))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("manage", manage_command)],
        states={
            1: [MessageHandler(filters.TEXT, select_user_command)],
            2: [CallbackQueryHandler(complete_user_callback, pattern="complete_user_callback_*"),
                CallbackQueryHandler(complete_task_callback, pattern="complete_task_callback_*_*"),
                CallbackQueryHandler(block_user_callback, pattern="block_user_callback_*"),
                CallbackQueryHandler(profile_user_callback, pattern="profile_user_callback_*"),
                CallbackQueryHandler(end_user_callback, pattern="end_user_callback_*")]
        },
        fallbacks=[CallbackQueryHandler(cancel_callback, pattern="cancel")]
    )
    application.add_handler(conv_handler)
    application.run_polling()


def add_test_tasks() -> None:
    database.add_task("Кто скрывается в тени?", 'Говорят, программисты умеют видеть красоту даже в скрытых деталях. Проверим?', 1, 'Говорят, программисты умеют видеть красоту даже в скрытых деталях. Проверим? Эта загадка, гораздо сложнее, чем "Куда делся пульт от телевизора?". Но что делает этот конкурс особенным, так это предметы, которые стоят рядом. Они будут твоими помощниками в создании произведения искусства. Возможности бесконечны, и творческий потенциал не ограничен!',
                      "1.jpg", "1 корпус 3 этаж")
    database.add_task("Зеркальный код", 'Настоящий вызов для твоих навыков анализа и понимания кода.', 1, 'В этот раз мы подготовили что-то особенное. Настоящий вызов для твоих навыков анализа и понимания кода. Ты готов попробовать? Придется смотреть дважды, чтобы понять, что здесь происходит!',
                      "2.jpg", "1 корпус 2 этаж")
    database.add_task("Перевертыши", 'Теперь мы проверим твою эрудицию и остроту ума.', 1, 'Теперь мы проверим твою эрудицию и остроту ума. Приготовься, ведь сейчас предстоит разгадывать загадки, покручивать мозговые извилины и искать скрытый смысл. А, может быть, "счастье" действительно "в глупости"?',
                      "3.jpg", "1 корпус 3 этаж")
    database.add_task("Параллельный запрос", 'Исследуй свою параллельность!', 1, 'Каждый студент знает, что такое параллельные запросы. Еще бы! Ведь только так можно одновременно справиться с лабораторной работой, открыв десятки вкладок в браузере, насладиться пиццей и краем глаза посмотреть сериал. А теперь, сможешь представить себе, что может быть интереснее, чем параллельный запрос для твоих рук?',
                      "4.jpg", "1 корпус 4 этаж")
    database.add_task("App quiz", 'Прими участие в App Quiz', 1, 'Языки программирования бывают двух видов: те, на которые все жалуются, и такие, на которых никто не пишет. А в каком IDE пишешь ты?',
                      "5.jpg", "1 корпус 2 этаж")
    database.add_task("Головоломки", 'Теперь придется потрудиться с настоящими головоломками.', 1, 'Казалось, что все головоломки и задачи позади. Теперь придется потрудиться с настоящими головоломками. В прямом смысле. С настоящими.',
                      "6.jpg", "1 корпус 4 этаж")
    database.add_task("Симметрия на плоскости", 'Говоришь, ты настоящий мастер симметрии и зеркальности? Пора это доказать!', 1, 'Говоришь, ты настоящий мастер симметрии и зеркальности? Значит этот конкурс специально для тебя! Мы нарисовали особую фигуру, а с тебя ее правильно отразить.',
                      "8.jpg", "1 корпус 2 этаж")


if __name__ == "__main__":
    main()
