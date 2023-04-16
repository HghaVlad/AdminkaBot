from bot import dp
from reqs import newpass, authenlink
from base_req import get_balance_andpaid_out
from filters.is_login import IsLogin, IsTarget
from filters.check_link import IsNewpasslink, Islink
from keyboards.keyboard import decline, gokeyb, user_menu, personal_account_keyb
from states.recover_pass import Newpass
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


@dp.message_handler(IsLogin(), Islink(), IsNewpasslink())
@dp.message_handler(IsLogin(), text='Изменить пароль')
@dp.message_handler(IsLogin(), commands=['newpass', 'recover'])
async def recover_pass(message: Message):
    await message.answer("<b>Введите новый пароль</b>", reply_markup=decline)
    await Newpass.pass1.set()


@dp.message_handler(state=Newpass.pass1)
async def retry_pass(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer("<b>Вы отменили изменение пароля</b>", reply_markup=user_menu(message.chat.id))
    elif len(message.text) < 6:
        await message.answer("<b>Пароль должен состоят из 6 и более символов</b>")
        await message.answer("<b>Введите пароль заново</b>")
    else:
        await state.update_data(pass1=message.text)
        await Newpass.pass2.set()
        await message.answer("<b>Повторите пароль</b>")


@dp.message_handler(state=Newpass.pass2)
async def check_pass(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text == 'Отмена':
        await state.finish()
        await message.answer("<b>Вы отменили изменение пароля</b>", reply_markup=user_menu(message.chat.id))
    elif user_data['pass1'] == message.text:
        newpass(message.chat.id, message.text)
        await state.finish()

        await message.answer("<b>Вы успешно изменили пароль ✅</b>", reply_markup=user_menu(message.chat.id))
    else:
        await message.answer("<b>Пароли не совпадают</b>")
        await message.answer("<b>Введите пароль заново</b>")


@dp.message_handler(IsLogin(), text='Авторизация')
@dp.message_handler(IsLogin(), commands=['login'])
async def auth_button(message: Message):
    link = authenlink(message.chat.id)
    keyb = gokeyb(link)
    await message.answer("<b>Отлично перейдите по ссылке, для авторизации:</b>", reply_markup=keyb)


@dp.message_handler(IsLogin(), text='Медиа Ресурсы')
@dp.message_handler(IsLogin(), commands=['media'])
async def media_resource(message: Message):
    await message.answer("<b>В процессе разработки</b>")


@dp.message_handler(IsLogin(), IsTarget(), text='Личный кабинет')
async def personal_acc(message: Message):
    res, adb = get_balance_andpaid_out(message.chat.id)
    await message.answer(f"<b>Личный кабинет:</b>\n\n<b>Рекламный бюджет:</b> {adb}₽\n\n<b>Баланс:</b> {res[0]}₽\n<b>Доступно к выводу:</b> {res[1]}₽", reply_markup=personal_account_keyb)


@dp.message_handler(IsLogin(), text='Личный кабинет')
async def personal_acc(message: Message):
    res = get_balance_andpaid_out(message.chat.id)
    await message.answer(f"<b>Личный кабинет:</b>\n\n<b>Баланс:</b> {res[0]}\n<b>Доступно к выводу:</b> {res[1]}", reply_markup=personal_account_keyb)
