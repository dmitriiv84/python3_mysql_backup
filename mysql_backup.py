#! /usr/bin/python3
# -*- coding: utf-8 -*-
#***********************************************************************************************************************
#
# Описание: Скрипт для создания бэкапа баз данных MySQL
#
# Версия: 1.0.0
#
# Автор: Дмитрий Видрашку
#
# Дата:  20016-06-13
#
# Email: dmitriiv84@gmail.com
#
#***********************************************************************************************************************
import time
import pymysql
import os
import argparse
import sys

CURR_DATE = time.strftime('%d-%m-%Y')
if sys.platform == 'linux':
    DUMP_PATH = '/usr/mysql_backup/' # Путь для создания бэкапа
elif sys.platform == 'win32':
    DUMP_PATH = "C:\\MySQL_Backup\\"
DATABASES = 'db_list' # Файл с названиями БД

# Подключение и настройка парсера аргментов коммандной строки
parser = argparse.ArgumentParser(description="Простой скрипт резервного копирования MySQL баз данных")
parser.add_argument('--rescan','-r',action="store_true",help="Пересканировать список БД, старый файл будет перезаписан",
                    default=False)
parser.add_argument('--host',type=str,default='127.0.0.1',help="IP хоста сервера БД MySQL")
parser.add_argument('--user','-u', type=str, default='root', help="Пользователь сервера БД MySQL."
                                                                  " По умолчанию 'root'")
parser.add_argument('--password','-p', type=str, default='root', help="Пароль пользователя сервера БД MySQL. "
                                                                         "По умолчанию 'root'")
options = vars(parser.parse_args())
USER = str(options['user'])
PASS = str(options['password'])
HOST = str(options['host'])
RESCAN = bool(options['rescan'])

try:
    conn = pymysql.connect(host='127.0.0.1', user=USER, passwd=PASS, db='mysql', charset='utf8')
except pymysql.MySQLError:
    print("Ошибка подключения к БД. Проверьте данные и попробуйте еще раз")
    exit(1)

cur = conn.cursor()
db_list = []

if not os.path.exists(DUMP_PATH):
    os.mkdir(DUMP_PATH)

if not os.path.exists(DUMP_PATH + CURR_DATE):
    os.mkdir(DUMP_PATH + CURR_DATE)

if RESCAN:   # Усли указан аргумент -r или --rescan
    f = open(DUMP_PATH + DATABASES, 'w')
    cur.execute("SHOW DATABASES;")
    for r in cur:
        db_name = str(r)
        db_name = db_name[2:len(db_name)-3]
        f.write (db_name + ';')
        db_list.append(db_name)
    cur.close()
    f.close()
elif not RESCAN: # Если не указан -r или --resccan
    if os.path.isfile(DUMP_PATH + DATABASES):
        f = open(DUMP_PATH + DATABASES)
        databases = f.read()
        databases = databases[:-1]
        db_list = databases.split(';')
        f.close()
    else:
        print('Файл не найден используйте скрипт с флагом -r для создания')
        exit(1)
for i in db_list:
    os.system("mysqldump -u" + USER + " -p" + PASS + " --skip-lock-tables " + " " + i + " > " + DUMP_PATH + CURR_DATE +
              "/" + i + ".sql")
conn.close()
print ("Бэкап закончен")
print ("Бэкап создан в  '" + DUMP_PATH + CURR_DATE + "' директории")
input('Для продолжения нажмите Enter')
exit(0)
