from bot import dp
from filters.is_login import IsLogin, IsTarget
from keyboards.keyboard import Analitpage1, Analitpage2, Analitpage3, backbut, user_menu, addcompanies, See_company_mark, See_promo_mark, Create_promo_company, Create_promo_program, Create_promo_program_finish, create_promo_see_list, promo_create_finish, decline, See_promo_marksells, compnay_expenses_keyb, deactivate_company_keyb, activate_company_keyb
from aiogram.dispatcher import FSMContext
from states.target import Analitpage, CreateCompany, See_company, See_promos, CreatePromo, Target_expense_group
from aiogram.types import Message, CallbackQuery
from base_req import checkname, createcompany, get_mycompany, get_about_company, get_mypromo, get_about_promo, select_promo_sells, get_about_target_analit, get_company_list, get_did_company, get_company_name, activate_company, deactivate_company, get_promonaes
from reqs import createnewpromo, create_target_expense

bot = dp.bot


@dp.message_handler(IsLogin(), IsTarget(), text='Аналитика')
async def target_analit(message: Message):
    await Analitpage.page1.set()
    state = dp.get_current().current_state()
    await state.update_data(Day=1)
    t1 = 'День'
    res = get_about_target_analit(1, 1, message.chat.id)
    if res[0] == 0:
        a1 = 0
        a2 = 0
    else:
        a1 = float('{:.2f}'.format(res[2] / res[0] * 100))
        a2 = float('{:.2f}'.format(res[3] / res[0]))

    await message.answer(text='<b>Аналитика</b>', reply_markup=backbut)
    await bot.send_message(chat_id=message.chat.id, text=f"<b>Продажи</b>\n"
                                                         f"<b>Дата:</b> {t1}\n\n"
                                                         f"<b>Продаж:</b> {res[0]}\n"
                                                         f"<b>Введено промокодов:</b> {res[1]}\n"
                                                         f"<b>Конверсия:</b> {a1}%\n"
                                                         f"<b>Стоимость ученика:</b> {a2}₽\n", reply_markup=Analitpage1)


async def analit_page(message: Message, state: FSMContext):
    current = await state.get_state()
    day = await state.get_data()
    if current == 'Analitpage:page1':
        await analitpage1(message, day['Day'])
    elif current == 'Analitpage:page2':
        await analitpage2(message, day['Day'])
    elif current == 'Analitpage:page3':
        await analitpage3(message, day['Day'])


async def analitpage1(message: Message, day):
    t1 = ''
    res = get_about_target_analit(1, day, message.chat.id)
    if res[0] == 0:
        a1 = 0
        a2 = 0
    else:
        a1 = float('{:.2f}'.format(res[2] / res[0] * 100))
        a2 = float('{:.2f}'.format(res[3] / res[0]))

    if day == 1:
        t1 = 'День'
    elif day == 7:
        t1 = "Неделя"
    elif day == 30:
        t1 = "Месяц"
    elif day == 725:
        t1 = 'Все время'
    await bot.edit_message_text(message_id=message.message_id, chat_id=message.chat.id, text=f"<b>Продажи</b>\n"
                                                                                             f"<b>Дата:</b> {t1}\n\n"
                                                                                             f"<b>Продаж:</b> {res[0]}\n"
                                                                                             f"<b>Введено промокодов:</b> {res[1]}\n"
                                                                                             f"<b>Конверсия:</b> {a1}%\n"
                                                                                             f"<b>Стоимость ученика:</b> {a2}₽\n", reply_markup=Analitpage1)


@dp.message_handler(IsTarget(), text='Назад', state=Analitpage)
async def analitback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Добро пожаловать</b>", reply_markup=user_menu(message.chat.id))


async def analitpage2(message: Message, day):
    t1 = ''
    res = get_about_target_analit(2, day, message.chat.id)
    if day == 1:
        t1 = 'День'
    elif day == 7:
        t1 = "Неделя"
    elif day == 30:
        t1 = "Месяц"
    elif day == 725:
        t1 = 'Все время'
    await bot.edit_message_text(message_id=message.message_id, chat_id=message.chat.id, text=f"<b>Рекламные компании</b>\n"
                                                                                             f"<b>Дата:</b> {t1}\n\n"
                                                                                             f"<b>Создано рекламных компаний:</b> {res[0]}\n\n"
                                                                                             f"<b>Создано промокодов:</b> {res[1]}\n"
                                                                                             f"<b>Удаленно промокодов:</b> {res[2]}\n"
                                                                                             f"<b>Активных промокодов:</b> {res[3]}\n", reply_markup=Analitpage2)


async def analitpage3(message: Message, day):
    t1 = ''
    if day == 1:
        t1 = 'День'
    elif day == 7:
        t1 = "Неделя"
    elif day == 30:
        t1 = "Месяц"
    elif day == 725:
        t1 = 'Все время'
    res = get_about_target_analit(3, day, message.chat.id)
    if len(res) == 0:
        t = f'<i>За данный период еще не было продаж</i>'
    else:
        t = ''
        for i in res:
            t = t + f'<i>{i[0]} - </i>{i[1]}\n'
    await bot.edit_message_text(message_id=message.message_id, chat_id=message.chat.id, text=f"<b>Продукты и продажи</b>\n"
                                                                                             f"<b>Дата:</b> {t1}\n\n{t}", reply_markup=Analitpage3)


@dp.callback_query_handler(lambda call: call.data and call.data.startswith("target_analit"), state=Analitpage)
async def analitbutt(call: CallbackQuery, state: FSMContext):
    if call.data == 'target_analitprev':
        current = await state.get_state()
        if current == 'Analitpage:page1':
            await Analitpage.page3.set()
        else:
            await Analitpage.previous()
        await analit_page(call.message, state)
    elif call.data == 'target_analit_next':
        current = await state.get_state()
        if current == 'Analitpage:page3':
            await Analitpage.page1.set()
        else:
            await Analitpage.next()
        await analit_page(call.message, state)
    elif call.data == 'target_analitDay':
        day = await state.get_data()
        if day['Day'] != 1:
            await state.update_data(Day=1)
            await analit_page(call.message, state)
    elif call.data == 'target_analitWeek':
        day = await state.get_data()
        if day['Day'] != 7:
            await state.update_data(Day=7)
            await analit_page(call.message, state)
    elif call.data == 'target_analitMonth':
        day = await state.get_data()
        if day['Day'] != 30:
            await state.update_data(Day=30)
            await analit_page(call.message, state)
    elif call.data == 'target_analitAll':
        day = await state.get_data()
        if day['Day'] != 725:
            await state.update_data(Day=725)
            await analit_page(call.message, state)


@dp.message_handler(IsTarget(), text='Рекламные компании')
async def adcomapnies(message: Message):
    await message.answer("<b>Рекламные компании</b>", reply_markup=addcompanies)


@dp.message_handler(IsTarget(), text='Создать рекламную компанию')
async def create_company(message: Message):
    await CreateCompany.name.set()
    await message.answer("<b>Введите название рекламной компании:</b>", reply_markup=decline)


@dp.message_handler(text='Отмена', state=CreateCompany)
async def comapnyback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Создание рекламной компании отменено</b>", reply_markup=addcompanies)


@dp.message_handler(IsTarget(), state=CreateCompany)
async def makecomapny(message: Message, state: FSMContext):
    allow = checkname(message.text)
    await state.finish()
    if allow is True:
        createcompany(message.text, message.chat.id)
        await message.answer("<b>Рекламная компания успешно создана ✅</b>", reply_markup=user_menu(message.chat.id))
    else:
        await message.answer("<b>Такое название уже есть</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(IsTarget(), text='Мои рекламные компании')
async def mycomapnis(message: Message):
    companies = get_mycompany(message.chat.id)
    if len(companies) == 0:
        await message.answer("<b>Вы еще не создали не одну компанию</b>")
    else:
        await See_company.set()
        state = dp.get_current().current_state()
        await state.update_data(list=companies, step=0, Day=1)
        company_id = companies[0]
        day = 1
        info = get_about_company(company_id, message.chat.id, day)
        t1 = ''
        if day == 1:
            t1 = 'День'
        elif day == 7:
            t1 = "Неделя"
        elif day == 30:
            t1 = "Месяц"
        elif day == 725:
            t1 = 'Все время'

        if info[2] == 0:
            a5 = 0
        else:
            a5 = info[4] / info[2]
        if info[3] == 0:
            a4 = 0
            a7 = 0
        else:
            a4 = info[2] / info[3] * 100
            a7 = info[4] / info[3]
        if info[4] == 0:
            a6 = 0
        else:
            a6 = (info[5] - info[4]) / info[4] * 100
        if info[8] == 0:
            a8 = ''
        else:
            a8 = f"<b>Заработано:</b> {info[8]}₽"
        await message.answer("<b>Рекламные компании</b>", reply_markup=backbut)
        await bot.send_message(chat_id=message.chat.id, text=f"<b>Название:</b> {info[0]}\n"
                                                             f"<b>Дата:</b> {t1}\n\n"
                                                             f"<b>Создано промокодов:</b> {info[1]}\n\n"
                                                             f"<b>Продаж:</b> {info[2]}\n"
                                                             f"<b>Введено промокодов:</b> {info[3]}\n"
                                                             f"<b>Конверсия:</b> {float('{:.2f}'.format(a4))}%\n\n"
                                                             f"<b>Стоимость ученика:</b> {float('{:.2f}'.format(a5))}\n"
                                                             f"<b>CPC:</b> {float('{:.2f}'.format(a7))}\n"
                                                             f"<b>Выручка:</b> {info[5]}\n"
                                                             f"<b>ROI</b> {float('{:.2f}'.format(a6))}%\n\n"
                                                             f"<b>Потрачено:</b> {info[4]}₽\n"
                                                             f"<b>Выручка:</b> {info[6]}₽\n\n{a8}", reply_markup=See_company_mark(1, len(companies), info[7]))


async def see_company(message: Message, state: FSMContext):
    user_data = await state.get_data()
    company_id = user_data['list'][user_data['step']]
    day = user_data['Day']
    info = get_about_company(company_id, message.chat.id, day)
    t1 = ''
    if day == 1:
        t1 = 'День'
    elif day == 7:
        t1 = "Неделя"
    elif day == 30:
        t1 = "Месяц"
    elif day == 725:
        t1 = 'Все время'

    a4, a5, a6, a7 = 0, 0, 0, 0
    if info[2] != 0:
        a5 = info[4] / info[2]
    if info[3] != 0:
        a4 = info[2] / info[3] * 100
        a7 = info[4] / info[3]
    if info[4] != 0:
        a6 = (info[5] - info[4]) / info[4] * 100
    if info[8] == 0:
        a8 = ''
    else:
        a8 = f"<b>Заработано:</b> {info[8]}₽"
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"<b>Название:</b> {info[0]}\n"
                                                                                             f"<b>Дата:</b> {t1}\n\n"
                                                                                             f"<b>Создано промокодов:</b> {info[1]}\n\n"
                                                                                             f"<b>Продаж:</b> {info[2]}\n"
                                                                                             f"<b>Введено промокодов:</b> {info[3]}\n"
                                                                                             f"<b>Конверсия:</b> {float('{:.2f}'.format(a4))}%\n\n"
                                                                                             f"<b>Стоимость ученика:</b> {float('{:.2f}'.format(a5))}\n"
                                                                                             f"<b>CPC:</b> {float('{:.2f}'.format(a7))}\n"
                                                                                             f"<b>Выручка:</b> {info[5]}\n"
                                                                                             f"<b>ROI</b> {float('{:.2f}'.format(a6))}%\n\n"
                                                                                             f"<b>Потрачено:</b> {info[4]}₽\n"
                                                                                             f"<b>Выручка:</b> {info[6]}₽\n\n{a8}", reply_markup=See_company_mark(user_data['step'] + 1, len(user_data['list']), info[7]))


@dp.message_handler(IsTarget(), text='Назад', state=See_company)
async def promotback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Добро пожаловать</b>", reply_markup=addcompanies)


@dp.callback_query_handler(lambda call: call.data and call.data.startswith("company_analit"), state=See_company)
async def company_analit(call: CallbackQuery, state: FSMContext):
    if call.data == 'company_analitprev':
        user_data = await state.get_data()
        if user_data['step'] > 0:
            await state.update_data(step=user_data['step'] - 1)
        else:
            await state.update_data(step=len(user_data['list'])-1)
        await see_company(call.message, state)
    elif call.data == 'company_analit_next':
        user_data = await state.get_data()
        if len(user_data['list']) > user_data['step'] + 1:
            await state.update_data(step=user_data['step'] + 1)
        else:
            await state.update_data(step=0)
        await see_company(call.message, state)
    elif call.data == 'company_analitDay':
        day = await state.get_data()
        if day['Day'] != 1:
            await state.update_data(Day=1)
            await see_company(call.message, state)
    elif call.data == 'company_analitWeek':
        day = await state.get_data()
        if day['Day'] != 7:
            await state.update_data(Day=7)
            await see_company(call.message, state)
    elif call.data == 'company_analitMonth':
        day = await state.get_data()
        if day['Day'] != 30:
            await state.update_data(Day=30)
            await see_company(call.message, state)
    elif call.data == 'company_analitAll':
        day = await state.get_data()
        if day['Day'] != 725:
            await state.update_data(Day=725)
            await see_company(call.message, state)

    elif call.data == 'company_analit_deactivate':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Вы уверены, что хотите деактивировать компанию?</b>", reply_markup=deactivate_company_keyb)
    elif call.data == 'company_analit_activate':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Вы уверены, что хотите активировать компанию?</b>", reply_markup=activate_company_keyb)
    elif call.data == 'company_analit_deactivateYes':
        user_data = await state.get_data()
        deactivate_company(user_data['list'][user_data['step']])
        await bot.send_message(call.message.chat.id, "<b>Вы успешно деактивировали компанию</b>")
        await see_company(call.message, state)
    elif call.data == 'company_analit_deactivateNo':
        await see_company(call.message, state)
    elif call.data == 'company_analit_activateYes':
        user_data = await state.get_data()
        activate_company(user_data['list'][user_data['step']])
        await bot.send_message(call.message.chat.id, "<b>Вы успешно активировали компанию</b>")
        await see_company(call.message, state)


@dp.message_handler(IsTarget(), text='Мои промокоды')
async def adpromos(message: Message):
    promocodes = get_mypromo(message.chat.id)
    if len(promocodes) == 0:
        await message.answer("<b>Вы еще не создали промокод</b>")
    else:
        await See_promos.set()
        state = dp.get_current().current_state()
        await state.update_data(list=promocodes, step=0, Day=1)
        info = get_about_promo(promocodes[0], 1)
        t1 = ''
        day = 1
        if day == 1:
            t1 = 'День'
        elif day == 7:
            t1 = "Неделя"
        elif day == 30:
            t1 = "Месяц"
        elif day == 725:
            t1 = 'Все время'

        if info[2] == 0:
            a3 = 0
        else:
            a3 = float('{:.2f}'.format(info[2] / info[1] * 100))
        if info[4] == 0:
            a4 = ''
        else:
            a4 = f"<b>Заработано:</b> {info[4]}"
        await message.answer("<b>Промокоды</b>", reply_markup=backbut)
        await bot.send_message(chat_id=message.chat.id, text=f"<b>Название:</b> {info[0]}\n"
                                                             f"<b>Дата:</b> {t1}\n\n"
                                                             f"<b>Вводов:</b> {info[1]}\n"
                                                             f"<b>Продаж:</b> {info[2]}\n"
                                                             f"<b>Конверсия:</b> {a3}%\n"
                                                             f"<b>Выручка:</b> {info[3]}\n\n{a4}",
                                                             reply_markup=See_promo_mark(1, len(promocodes)))


async def see_promo(message: Message, state: FSMContext):
    user_data = await state.get_data()
    day = user_data['Day']
    promo_id = user_data['list'][user_data['step']]
    info = get_about_promo(promo_id, day)
    t1 = ''
    if day == 1:
        t1 = 'День'
    elif day == 7:
        t1 = "Неделя"
    elif day == 30:
        t1 = "Месяц"
    elif day == 725:
        t1 = 'Все время'

    if info[2] == 0:
        a3 = 0
    else:
        a3 = float('{:.2f}'.format(info[2] / info[1] * 100))
    if info[4] == 0:
        a4 = ''
    else:
        a4 = f"<b>Заработано:</b> {info[4]}"
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"<b>Название:</b> {info[0]}\n"
                                                                                             f"<b>Дата:</b> {t1}\n\n"
                                                                                             f"<b>Вводов:</b> {info[1]}\n"
                                                                                             f"<b>Продаж:</b> {info[2]}\n"
                                                                                             f"<b>Конверсия:</b> {a3}%\n"
                                                                                             f"<b>Выручка:</b> {info[3]}\n\n{a4}", reply_markup=See_promo_mark(user_data['step']+1, len(user_data['list'])))


async def see_promo_sells(message: Message, user_data):
    res = select_promo_sells(user_data['list'][user_data['step']], user_data['Day'])
    t1 = '<b>Продажи</b>\n\n'
    for name, amount in res:
        t1 = t1 + f'<b>{name}:</b> {amount}₽\n'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=t1, reply_markup=See_promo_marksells())


@dp.callback_query_handler(lambda call: call.data and call.data.startswith("promo_analit"), state=See_company)
async def promo_analit(call: CallbackQuery, state: FSMContext):
    if call.data == 'promo_analitprev':
        user_data = await state.get_data()
        if user_data['step'] > 0:
            await state.update_data(step=user_data['step'] - 1)
        else:
            await state.update_data(step=len(user_data['list'])-1)
        await see_promo(call.message, state)
    elif call.data == 'promo_analit_next':
        user_data = await state.get_data()
        if len(user_data['list']) > user_data['step'] + 1:
            await state.update_data(step=user_data['step'] + 1)
        else:
            await state.update_data(step=0)
        await see_promo(call.message, state)
    elif call.data == 'promo_analitDay':
        day = await state.get_data()
        if day['Day'] != 1:
            await state.update_data(Day=1)
            await see_promo(call.message, state)
    elif call.data == 'promo_analitWeek':
        day = await state.get_data()
        if day['Day'] != 7:
            await state.update_data(Day=7)
            await see_promo(call.message, state)
    elif call.data == 'promo_analitMonth':
        day = await state.get_data()
        if day['Day'] != 30:
            await state.update_data(Day=30)
            await see_promo(call.message, state)
    elif call.data == 'promo_analitAll':
        day = await state.get_data()
        if day['Day'] != 725:
            await state.update_data(Day=725)
            await see_promo(call.message, state)

    elif call.data == 'promo_analitsells':
        user_data = await state.get_data()
        promo_id = user_data['list'][user_data['step']]
        res = select_promo_sells(promo_id, user_data['Day'])
        if len(res) > 0:
            await see_promo_sells(call.message,  user_data)
        else:
            await call.answer("За данный период нет никаких продаж")
    elif call.data == 'promo_analitSellDay':
        user_data = await state.get_data()
        if user_data['Day'] != 1:
            await state.update_data(Day=1)
            await see_promo_sells(call.message, user_data)
    elif call.data == 'promo_analitSellWeek':
        user_data = await state.get_data()
        if user_data['Day'] != 7:
            await state.update_data(Day=7)
            await see_promo_sells(call.message, user_data)
    elif call.data == 'promo_analitSellMonth':
        user_data = await state.get_data()
        if user_data['Day'] != 30:
            await state.update_data(Day=30)
            await see_promo_sells(call.message, user_data)
    elif call.data == 'promo_analitSellAll':
        user_data = await state.get_data()
        if user_data['Day'] != 725:
            await state.update_data(Day=725)
        await see_promo_sells(call.message, user_data)
    elif call.data == 'promo_analitback':
        await see_promo(call.message, state)


@dp.message_handler(IsTarget(), text='Назад', state=See_promos)
async def analitback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Добро пожаловать</b>", reply_markup=addcompanies)


@dp.message_handler(IsTarget(), text='Создать промокод')
async def create_promo(message: Message):
    await message.answer("<b>Придумайте название промокода:</b>", reply_markup=decline)
    await CreatePromo.name.set()


@dp.message_handler(text='Отмена', state=CreatePromo)
async def comapnyback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Создание промокода отменено</b>", reply_markup=addcompanies)


@dp.message_handler(state=CreatePromo.name)
async def create_promo_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    if get_promonaes(message.text) is True:
        await message.answer("<b>Промокод с таким названием уже существует</b>")
        await message.answer("<b>Введите название промокода</b>")
    else:
        await CreatePromo.company.set()
        await message.answer("<b>Выберите рекламную компанию:</b>", reply_markup=Create_promo_company(message.chat.id))


@dp.callback_query_handler(lambda call: call.data and call.data.startswith("promo_create"), state=CreatePromo)
async def promo_create_callback(call: CallbackQuery, state: FSMContext):
    if call.data.startswith("promo_create_comapny"):
        cid = int(call.data.split("=")[1])
        await state.update_data(company_id=cid)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await CreatePromo.discount.set()
        await bot.send_message(call.message.chat.id, text="<b>Какая скидка у рекламного промокода?</b>", reply_markup=decline)
    elif call.data.startswith("promo_create_program"):
        pid = int(call.data.split("=")[1])
        user_data = await state.get_data()
        programlist = user_data['prog_list']
        if pid in programlist:
            programlist.remove(pid)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=Create_promo_program_finish(programlist))
            await state.update_data(prog_list=programlist)
        else:
            programlist.append(pid)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=Create_promo_program_finish(programlist))
            await state.update_data(prog_list=programlist)
    elif call.data == 'promo_create_finishprog':
        user_data = await state.get_data()
        if len(user_data['prog_list']) == 1:
            user_data = await state.get_data()
            await state.update_data(watch_list=user_data['prog_list'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"<b>Промокод\n\n</b>"
                                             f"<b>Название:</b> {user_data['name']}\n"
                                             f"<b>Скидка:</b> {user_data['discount']}%",
                                        reply_markup=promo_create_finish)

        else:
            await CreatePromo.watch_list.set()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Создайте очередь показов продуктов</b>\n<b>Какой продукт показывать первым?</b>", reply_markup=create_promo_see_list(user_data['prog_list'], user_data['watch_list']))

    elif call.data.startswith("promo_create_showpro"):
        pid = int(call.data.split("=")[1])
        user_data = await state.get_data()
        watch_list = user_data['watch_list']
        if pid in watch_list:
            watch_list.remove(pid)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Создайте очередь показов продуктов</b>\n<b>Какой продукт показывать следующим?</b>", reply_markup=create_promo_see_list(user_data['prog_list'], watch_list))
            await state.update_data(watch_list=watch_list)
        else:
            watch_list.append(pid)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Создайте очередь показов продуктов</b>\n<b>Какой продукт показывать следующим?</b>", reply_markup=create_promo_see_list(user_data['prog_list'], watch_list))
            await state.update_data(watch_list=watch_list)
    elif call.data == 'promo_create_finish':
        user_data = await state.get_data()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"<b>Промокод\n\n</b>"
                                                                                                           f"<b>Название:</b> {user_data['name']}\n"
                                                                                                           f"<b>Скидка:</b> {user_data['discount']}%", reply_markup=promo_create_finish)
    elif call.data == 'promo_create_finish_end':
        user_data = await state.get_data()
        createnewpromo(user_data, call.message.chat.id)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, "<b>Промокод успешно создан ✅</b>", reply_markup=addcompanies)
        await state.finish()
    elif call.data == 'promo_create_decline':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, "<b>Вы отменили создание промокода ❌</b>", reply_markup=addcompanies)
        await state.finish()


@dp.message_handler(state=CreatePromo.discount)
async def create_promo_percent(message: Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) < 5:
            await message.answer("<b>Скидка должна быть больше 5%</b>")
            await message.answer("<b>Введите скидку еще раз</b>")
        elif int(message.text) > 30:
            await message.answer("<b>Скидка должна быть меньше 30%</b>")
            await message.answer("<b>Введите скидку еще раз</b>")
        else:
            await state.update_data(discount=int(message.text), prog_list=[], watch_list=[])
            await CreatePromo.programs.set()
            await message.answer("<b>Выберите продукты на которые он действует</b>", reply_markup=Create_promo_program())


@dp.message_handler(text='Назад в меню', state=Analitpage)
async def analitback(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Добро пожаловать</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(text='Назад в меню')
async def analitback(message: Message, state: FSMContext):
    await message.answer("<b>Добро пожаловать</b>", reply_markup=user_menu(message.chat.id))


@dp.message_handler(IsLogin(), IsTarget(), text='Расходы на компании')
async def company_expenses(message: Message):
    res = get_company_list(message.chat.id)
    if len(res) == 0:
        await message.answer("<b>Пока что нет компаний, за которые надо указать потраченный бюджет</b>")
    else:
        expenses_keyboard = compnay_expenses_keyb(res)
        await message.answer("<b>Компании за которые надо указать потраченный бюджет</b>", reply_markup=expenses_keyboard)


@dp.callback_query_handler(lambda call: call.data and call.data.startswith("target_company"))
async def company_expenses_callback(call: CallbackQuery):
    if call.data.startswith("target_company_expense_add"):
        cid = call.data.split("?")[1]
        day = get_did_company(cid)
        if day == 'no':
            await call.answer("Вам не надо указывать расходы за данную компанию")
        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            name = get_company_name(cid)[0]
            await bot.send_message(chat_id=call.message.chat.id, text=f"<b>Введите расход за компанию </b> {name} <b>в период</b> {day}", reply_markup=decline)
            await Target_expense_group.main.set()
            state = dp.get_current().current_state()
            await state.update_data(cid=cid, date=day)


@dp.message_handler(state=Target_expense_group.main)
async def get_target_expens(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer("<b>Вы отменили ввод расхода</b>", reply_markup=user_menu(message.chat.id))
    elif message.text.isdigit():
        user_data = await state.get_data()
        create_target_expense(user_data['cid'], int(message.text), message.chat.id, user_data['date'])
        await message.answer("<b>Вы успешно ввели расход</b>", reply_markup=user_menu(message.chat.id))
        await state.finish()
        await company_expenses(message)
    else:
        await message.answer("<b>Введите расход только числом\n</b><i>Например:</i> 2000")


@dp.message_handler(IsLogin(), text='Назад')
async def main_menuBack(message: Message):
    await message.answer("<b>Добро пожаловать</b>", reply_markup=user_menu(message.chat.id))
