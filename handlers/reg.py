from bot import dp, base_db, base_host, base_user, base_password
from reqs import newuser
from keyboards.keyboard import user_menu
from filters.check_link import Islink, IsReglink
from filters.is_login import IsLogin, IsNotLogin
from aiogram.types import Message, ReplyKeyboardRemove
import pymysql as sq


@dp.message_handler(commands="test1")
async def cmd_test1(message: Message):
    await message.reply("Test 1")


@dp.message_handler(Islink(), IsReglink())
async def register(message: Message):
    code = message.text.split()[1].split("_")[1]
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT username FROM admin_panel_user WHERE telegram_id = %s ", (message.chat.id,))
        username = cur.fetchone()
        if username is None:
            cur.execute(f"SELECT req_id FROM admin_panel_pre_user WHERE req_id = (SELECT id FROM admin_panel_tg_requests WHERE code = %s )", (code,))
            pre_user = cur.fetchone()
            if pre_user is None:
                await message.answer('<b>Неизвестный код</b>', parse_mode='Markdown')
            else:
                cur.execute(f"UPDATE admin_panel_tg_requests SET user_id = %s WHERE id = %s ", (message.chat.id, pre_user[0]))
                con.commit()
                newuser(message.chat.id, code)
                await message.answer("<b>Вы успешно зарегистрироаны ✅\n</b>", reply_markup=user_menu(message.chat.id))
        else:
            await message.answer("<b>Вы уже зарегистрированы</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(IsLogin(), commands=['start'])
async def hello(message: Message):
    await message.answer("<b>Добро пожаловать</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(IsLogin())
async def nocommand(message: Message):
    await message.answer("<b>Неизвестная команда</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(IsNotLogin())
async def anything(message: Message):
    await message.answer("<b>Хмм..</b>\n" +
                         "<i>Я не вижу тебя в базе, у меня есть подозрения что ты не в команде Brain University.</i>")
    await message.answer("<b>Если ты считаешь что ты можешь быть полезен проекту пришли резюме на email.</b>\nHr@brainuniversity.ru", reply_markup=ReplyKeyboardRemove())
