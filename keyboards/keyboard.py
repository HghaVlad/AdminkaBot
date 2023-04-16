from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from base_req import selectrole, select_names_comapny, select_names_program, select_program_name


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row("Авторизация", "Изменить пароль")


target_menu = ReplyKeyboardMarkup(resize_keyboard=True)
target_menu.row("Личный кабинет", "Аналитика")
target_menu.row("Рекламные компании", "Расходы на компании")


personal_account_keyb = ReplyKeyboardMarkup(resize_keyboard=True)
personal_account_keyb.row("Авторизация", "Изменить пароль")
personal_account_keyb.row("Назад в меню")

decline = ReplyKeyboardMarkup(resize_keyboard=True)
decline.row("Отмена")


def gokeyb(link):
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton(text='Перейти', url=link))
    return keyb


def user_menu(t_id):
    user_role = selectrole(t_id)[0]
    if user_role == 'Target':
        return target_menu
    else:
        return main_menu


backbut = ReplyKeyboardMarkup(resize_keyboard=True)
backbut.row("Назад")

Analitpage1 = InlineKeyboardMarkup(row_width=4)
Analitpage1.add(InlineKeyboardButton(text='⬅', callback_data='target_analitprev'), InlineKeyboardButton(text='1/3', callback_data='pass'), InlineKeyboardButton(text='➡', callback_data='target_analit_next'))
Analitpage1.row(InlineKeyboardButton(text='День', callback_data='target_analitDay'), InlineKeyboardButton(text='Неделя', callback_data='target_analitWeek'), InlineKeyboardButton(text='Месяц', callback_data='target_analitMonth'), InlineKeyboardButton(text='Все время', callback_data='target_analitAll'))

Analitpage2 = InlineKeyboardMarkup(row_width=4)
Analitpage2.add(InlineKeyboardButton(text='⬅', callback_data='target_analitprev'), InlineKeyboardButton(text='2/3', callback_data='pass'), InlineKeyboardButton(text='➡', callback_data='target_analit_next'))
Analitpage2.row(InlineKeyboardButton(text='День', callback_data='target_analitDay'), InlineKeyboardButton(text='Неделя', callback_data='target_analitWeek'), InlineKeyboardButton(text='Месяц', callback_data='target_analitMonth'), InlineKeyboardButton(text='Все время', callback_data='target_analitAll'))

Analitpage3 = InlineKeyboardMarkup(row_width=4)
Analitpage3.add(InlineKeyboardButton(text='⬅', callback_data='target_analitprev'), InlineKeyboardButton(text='3/3', callback_data='pass'), InlineKeyboardButton(text='➡', callback_data='target_analit_next'))
Analitpage3.row(InlineKeyboardButton(text='День', callback_data='target_analitDay'), InlineKeyboardButton(text='Неделя', callback_data='target_analitWeek'), InlineKeyboardButton(text='Месяц', callback_data='target_analitMonth'), InlineKeyboardButton(text='Все время', callback_data='target_analitAll'))


addcompanies = ReplyKeyboardMarkup(resize_keyboard=True)
addcompanies.row("Мои рекламные компании", "Создать рекламную компанию")
addcompanies.row("Мои промокоды", "Создать промокод")
addcompanies.row("Назад в меню")


def See_company_mark(now, maxim, active):
    see_company_markup = InlineKeyboardMarkup(row_width=4)
    see_company_markup.row(InlineKeyboardButton(text='⬅', callback_data='company_analitprev'), InlineKeyboardButton(text=str(now) + '/' + str(maxim), callback_data='pass'), InlineKeyboardButton(text='➡', callback_data='company_analit_next'))
    if active == 1:
        see_company_markup.add(InlineKeyboardButton(text='Деактивировать', callback_data='company_analit_deactivate'))
    else:
        see_company_markup.add(InlineKeyboardButton(text='Активировать', callback_data='company_analit_activate'))
    see_company_markup.row(InlineKeyboardButton(text='День', callback_data='company_analitDay'), InlineKeyboardButton(text='Неделя', callback_data='company_analitWeek'), InlineKeyboardButton(text='Месяц', callback_data='company_analitMonth'), InlineKeyboardButton(text='Все время', callback_data='company_analitAll'))
    return see_company_markup


def See_promo_mark(now, maxim):
    see_promo_markup = InlineKeyboardMarkup(row_width=4)
    see_promo_markup.row(InlineKeyboardButton(text='⬅', callback_data='promo_analitprev'), InlineKeyboardButton(text=str(now) + '/' + str(maxim), callback_data='pass'), InlineKeyboardButton(text='➡', callback_data='promo_analit_next'))
    see_promo_markup.row(InlineKeyboardButton(text='Продажи', callback_data='promo_analitsells'))
    see_promo_markup.row(InlineKeyboardButton(text='День', callback_data='promo_analitDay'), InlineKeyboardButton(text='Неделя', callback_data='promo_analitWeek'), InlineKeyboardButton(text='Месяц', callback_data='promo_analitMonth'), InlineKeyboardButton(text='Все время', callback_data='promo_analitAll'))
    return see_promo_markup


def See_promo_marksells():
    see_promo_markup = InlineKeyboardMarkup(row_width=4)
    see_promo_markup.row(InlineKeyboardButton(text='Назад', callback_data='promo_analitback'))
    see_promo_markup.row(InlineKeyboardButton(text='День', callback_data='promo_analitSellDay'), InlineKeyboardButton(text='Неделя', callback_data='promo_analitSellWeek'), InlineKeyboardButton(text='Месяц', callback_data='promo_analitSellMonth'), InlineKeyboardButton(text='Все время', callback_data='promo_analitSellAll'))
    return see_promo_markup


def Create_promo_company(t_id):
    names = select_names_comapny(t_id)
    comapnies_keyboard = InlineKeyboardMarkup(row_width=1)
    for name, cid in names:
        comapnies_keyboard.add(InlineKeyboardButton(text=name, callback_data='promo_create_comapny='+str(cid)))
    return comapnies_keyboard


def Create_promo_program():
    names = select_names_program()
    programs_keyboard = InlineKeyboardMarkup(row_width=1)
    for name, pid in names:
        programs_keyboard.add(InlineKeyboardButton(text=name, callback_data='promo_create_program='+str(pid)))
    return programs_keyboard


def Create_promo_program_finish(prog_list):
    names = select_names_program()
    programs_keyboard = InlineKeyboardMarkup(row_width=1)
    for name, pid in names:
        if pid in prog_list:
            programs_keyboard.add(InlineKeyboardButton(text=name + ' ✅', callback_data='promo_create_program=' + str(pid)))
        else:
            programs_keyboard.add(
                InlineKeyboardButton(text=name, callback_data='promo_create_program=' + str(pid)))
    if len(prog_list) > 0:
        programs_keyboard.row(InlineKeyboardButton(text='Готово', callback_data='promo_create_finishprog'))
    return programs_keyboard


def create_promo_see_list(prog_list, watch_list):
    programs_keyboard = InlineKeyboardMarkup(row_width=1)
    for pid in prog_list:
        if pid not in watch_list:
            name = select_program_name(pid)
            programs_keyboard.add(InlineKeyboardButton(text=name, callback_data='promo_create_showpro='+str(pid)))
    if len(watch_list) >= 2:
        programs_keyboard.add(InlineKeyboardButton(text='Готово', callback_data='promo_create_finish'))
    return programs_keyboard


promo_create_finish = InlineKeyboardMarkup()
promo_create_finish.add(InlineKeyboardButton(text='Создать', callback_data='promo_create_finish_end'), InlineKeyboardButton(text='Отменить', callback_data='promo_create_decline'))


def compnay_expenses_keyb(res):
    expenses_keyboard = InlineKeyboardMarkup()
    for name, cid in res:
        expenses_keyboard.add(InlineKeyboardButton(text=name, callback_data='target_company_expense_add?'+str(cid)))
    return expenses_keyboard


activate_company_keyb = InlineKeyboardMarkup()
activate_company_keyb.add(InlineKeyboardButton(text='Да', callback_data='company_analit_activateYes'), InlineKeyboardButton(text='Нет', callback_data='company_analit_deactivateNo'))

deactivate_company_keyb = InlineKeyboardMarkup()
deactivate_company_keyb.add(InlineKeyboardButton(text='Да', callback_data='company_analit_deactivateYes'), InlineKeyboardButton(text='Нет', callback_data='company_analit_deactivateNo'))
