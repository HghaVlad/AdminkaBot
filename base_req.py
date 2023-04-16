import pymysql as sq
import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read("config.ini")
base_user = config['Telegram']['database_user']
base_password = config['Telegram']['database_password']
base_host = config['Telegram']['database_host']
base_db = config['Telegram']['database_name']
target_account = config['Pay']['target_account_id']


def selectrole(cid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT role FROM admin_panel_user WHERE telegram_id = %s AND iswork = 1", (cid,))
        username = cur.fetchone()
        return username


def checkname(name):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name FROM admin_panel_target_company WHERE name = %s ", (name,))
        name = cur.fetchone()
        return name is None


def createcompany(name, t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO admin_panel_target_company(name, t_id, Date) VALUES (%s, %s, %s)", (name, t_id, datetime.now()))
        cur.execute(f"INSERT INTO Actions(t_id, Name, Act, Date) VALUES(%s, %s, 'Target_create_company', %s ) ", (t_id, name, datetime.now()))
        con.commit()


def get_mycompany(t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM admin_panel_target_company WHERE t_id = %s ", (t_id,))
        companies = [int(x[0]) for x in cur.fetchall()]
        return companies


def get_about_company(company_id: int, t_id: int, day: int):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT (SELECT name FROM admin_panel_target_company WHERE id = {company_id} ) as a0, (SELECT count(*) FROM admin_panel_target_promocodes WHERE Company_id = {company_id} ) as a1, (SELECT count(*) FROM apiapp_promoactiv WHERE Promo_name in (SELECT name FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Company_id = {company_id}) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a2, (SELECT count(*) FROM Actions WHERE Act = 'Target_promo_activ' AND Name in (SELECT name FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Company_id = {company_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY ) ) as a3, (SELECT IFNULL(sum(cost),0) FROM admin_panel_target_expenses WHERE company_id = {company_id} AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a4, (SELECT IFNULL(sum(Amount),0) FROM apiapp_promoactiv WHERE Promo_tp = 'Специальный' AND Promo_name in (SELECT name FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Company_id = {company_id}) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a5, (SELECT IFNULL(sum(Expert_comis),0) FROM apiapp_orders WHERE PromoName in (SELECT CONCAT('Специальный_', name) FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Company_id = {company_id}) AND  Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a6, (SELECT Active FROM admin_panel_target_company WHERE id = {company_id}) as a7, (SELECT IFNULL(sum(Target_comis),0) FROM apiapp_orders WHERE PromoName in (SELECT CONCAT('Специальный_', name) FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Company_id = {company_id}) AND  Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY ) ) as a8")
        res = cur.fetchone()
        return res


def get_mypromo(t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM admin_panel_target_promocodes WHERE t_id = %s ", (t_id,))
        promos = [int(x[0]) for x in cur.fetchall()]
        return promos


def checkpromoname(name):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name FROM LB_promo UNION SELECT text FROM promocodes UNION SELECT name FROM admin_panel_target_promocodes")
        other_promocodes_sorted = [x[0] for x in cur.fetchall()]
        return name not in other_promocodes_sorted


def get_about_promo(promo_id: int, day: int):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT (SELECT name FROM admin_panel_target_promocodes WHERE id = {promo_id} ) as a0, (SELECT count(*) FROM Actions WHERE Act = 'Target_promo_activ' AND Name = (SELECT name FROM admin_panel_target_promocodes WHERE id = {promo_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a1, (SELECT count(*) FROM apiapp_promoactiv WHERE Promo_name = (SELECT name FROM admin_panel_target_promocodes WHERE id = {promo_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a2, (SELECT IFNULL(sum(Amount),0) FROM apiapp_promoactiv WHERE Promo_name = (SELECT name FROM admin_panel_target_promocodes WHERE id = {promo_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY ) ) as a3, (SELECT IFNULL(sum(Target_comis),0) FROM apiapp_orders WHERE PromoName = 'Специальный_' + (SELECT name FROM admin_panel_target_promocodes WHERE id = {promo_id}) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a4")
        res = cur.fetchone()
        return res


def select_names_comapny(t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name, id FROM admin_panel_target_company WHERE t_id = %s", (t_id,))
        companies = cur.fetchall()
        return companies


def select_names_program():
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name, id FROM programs WHERE archived = 0 ")
        programs = cur.fetchall()
        return programs


def select_program_name(pid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name FROM programs WHERE id = {pid} ")
        name = cur.fetchone()
        return name[0]


def select_promo_sells(promo, day):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name FROM admin_panel_target_promocodes WHERE id =  {promo}")
        name = cur.fetchone()[0]
        cur.execute(f"SELECT GoodName, sum(Amount) FROM apiapp_orders WHERE PromoName = 'Специальный_{name}' and Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY ) GROUP BY GoodName ")
        res = cur.fetchall()
        return res


def get_about_target_analit(page, day, t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        if page == 1:
            cur.execute(f"SELECT (SELECT count(*) FROM apiapp_promoactiv WHERE Promo_name in (SELECT name FROM admin_panel_target_promocodes WHERE t_id = {t_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a0, (SELECT count(*) FROM Actions WHERE Act = 'Target_promo_activ' AND Author_id = {t_id} AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a1, (SELECT count(*) FROM apiapp_orders WHERE Goodtype = 'Образовательная программа' AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a2, (SELECT IFNULL(sum(cost),0) FROM admin_panel_target_expenses WHERE user_id = (SELECT id FROM admin_panel_user WHERE telegram_id = {t_id} ) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a3")
            res = cur.fetchone()
        elif page == 2:
            cur.execute(f"SELECT (SELECT count(*) FROM Actions WHERE Act = 'Target_create_company' AND t_id = {t_id} AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a0, (SELECT count(*) FROM Actions WHERE Act = 'Target_create_promo' AND t_id = {t_id} AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a1, (SELECT count(*) FROM Actions WHERE Act = 'Target_delete_promo' AND t_id = {t_id} AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY )) as a2, (SELECT count(*) FROM admin_panel_target_promocodes WHERE t_id = {t_id} AND Activates > 0 ) as a3")
            res = cur.fetchone()
        elif page == 3:
            cur.execute(f"SELECT (SELECT name FROM programs WHERE id = Good_id), count(DISTINCT Good_id) FROM apiapp_promoactiv WHERE Promo_name in (SELECT name FROM admin_panel_target_promocodes WHERE t_id = {t_id}) AND Date >= DATE_ADD(NOW(), INTERVAL -{day} DAY ) GROUP BY Good_id")
            res = cur.fetchall()
        return res


def get_company_list(t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name, id FROM admin_panel_target_company as a WHERE (SELECT company_id FROM admin_panel_target_expenses WHERE company_id = a.id AND CAST(Date as Date) = CAST(NOW() as Date )) is NULL AND t_id = {t_id} AND Active = 1")
        res = cur.fetchall()
        return res


def get_did_company(cid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT CAST(Date as Date) FROM admin_panel_target_expenses WHERE company_id = {cid} ORDER BY Date DESC")
        res = cur.fetchone()
        if res is None:
            cur.execute(f"SELECT CAST(Date as Date) FROM admin_panel_target_company WHERE id = {cid}")
            return cur.fetchone()[0]
        else:
            if res[0] == datetime.today().date():
                return 'no'
            else:
                return res[0] + timedelta(days=1)


def get_company_name(cid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT name FROM admin_panel_target_company WHERE id = {cid}")
        name = cur.fetchone()
        return name


def deactivate_company(cid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE admin_panel_target_company SET Active = 0 WHERE id = {cid}")
        con.commit()


def activate_company(cid):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE admin_panel_target_company SET Active = 1 WHERE id = {cid}")
        con.commit()


def get_promonaes(name):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM LB_promo UNION SELECT text FROM promocodes UNION select name from admin_panel_target_promocodes ")
        other_promocodes = cur.fetchall()
        other_promocodes_sorted = [x[0] for x in other_promocodes]
        return name in other_promocodes_sorted or name in ('no', 'Акция')


def get_balance_andpaid_out(t_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT balance, can_paid_out FROM admin_panel_user WHERE telegram_id = {t_id}")
        info = cur.fetchone()
        return info, get_balanceaccount()


def get_balanceaccount():
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT balance FROM admin_panel_payment_accounts WHERE Account_number = {target_account}")
        info = cur.fetchone()
        return info[0]
