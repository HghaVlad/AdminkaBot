from aiogram.dispatcher.filters.state import State, StatesGroup


class Analitpage(StatesGroup):
    page1 = State()
    page2 = State()
    page3 = State()


class CreateCompany(StatesGroup):
    name = State()


class CreatePromo(StatesGroup):
    name = State()
    company = State()
    discount = State()
    programs = State()
    watch_list = State()


See_company = State()
See_promos = State()


class Target_expense_group(StatesGroup):
    main = State()
