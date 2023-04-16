import requests
import pymysql as sq
import configparser
from datetime import datetime
config = configparser.ConfigParser()
config.read("config.ini")
bot_token = config['Telegram']['Adminka_bot_token']
base_user = config['Telegram']['database_user']
base_password = config['Telegram']['database_password']
base_host = config['Telegram']['database_host']
base_db = config['Telegram']['database_name']
authen = config['Pay']['auth']


def newuser(chat_id, code):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT `key` FROM apiapp_apikeys WHERE id = 1")
        key = cur.fetchone()[0]
        requests.post("https://api.brainuniversity.ru/adminka_preuser/", json={'auth': authen, 'key': key, 't_id': chat_id, "code": code})
        return "OK"


def newpass(chat_id, password):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT `key` FROM apiapp_apikeys WHERE id = 1")
        key = cur.fetchone()[0]
        requests.post("https://api.brainuniversity.ru/adminka_newpass/", json={'auth': authen, 'key': key, 't_id': chat_id, "newpass": password})


def authenlink(chat_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT `key` FROM apiapp_apikeys WHERE id = 1")
        key = cur.fetchone()[0]
        resp = requests.post("https://api.brainuniversity.ru/adminka_newauth/", json={'auth': authen, 'key': key, 't_id': chat_id})
        resp = resp.json()
        link = "https://cp.brainuniversity.ru/login_tg/"+str(resp['res'])

        return link


def createnewpromo(data, chat_id):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT `key` FROM apiapp_apikeys WHERE id = 1")
        key = cur.fetchone()[0]
        goods = ','.join([str(x) for x in data['prog_list']])
        watch_list = ','.join([str(x) for x in data['watch_list']])
        requests.post("https://api.brainuniversity.ru/target_newpromo/", json={'auth': authen, 'key': key, 'name': data['name'], 't_id': chat_id, 'Goods': goods, 'watch_list': watch_list, 'company': data['company_id'], 'Discount': data['discount']})
        cur.execute(f"INSERT INTO Actions(t_id, Name, Act, Date) VALUES(%s, %s, %s, %s ) ", (chat_id, data['name'], datetime.now()))
        con.commit()


def create_target_expense(cid, cost, t_id, day):
    with sq.connect(host=base_host, user=base_user, password=base_password, database=base_db) as con:
        cur = con.cursor()
        cur.execute("SELECT `key` FROM apiapp_apikeys WHERE id = 1")
        key = cur.fetchone()[0]
        if day == datetime.today().date():
            date = 'no'
        else:
            date = day
        requests.post("https://api.brainuniversity.ru/target_newexpense/", json={'auth': authen, 'key': key, 'cid': cid, 'cost': cost, 't_id': t_id, 'date': str(date)})
        cur.execute(f"INSERT INTO Actions(t_id, Name, Act, Date) VALUES(%s, %s, 'Target_create_new_expense', %s ) ", (t_id, cid, datetime.now()))
        con.commit()
