import csv
import os.path
import subprocess
from datetime import datetime
from dateutil import parser
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

current_user = subprocess.run(['whoami'], capture_output=True, text=True).stdout.replace('\n', '')
flatpakway = 'sqlite:////' + 'home/' + current_user + '/.var/app/io.github.alainm23.planify/data/io.github.alainm23.planify/database.db'
engine = create_engine(flatpakway, echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()


def ans_start():
    if os.path.exists(flatpakway[10:]) == True:
        print('До импорта задач необходимо положить рядом с py-скриптом файл 1.csv,')
        print("внутри которого лежат экспортированные из Tick-Tick'а задачи")
        print('Скрипт определил, что файл базы данных Planify находится по пути:')
        print(flatpakway[10:])
        otvet = input('все верно? y/n ')
        ans_confirmway(otvet)
    else:
        ans_askway()

def ans_askway():
    newflatpakway = input('Введите полный (абсолютный) путь к файлу database.db: ')
    if os.path.exists(newflatpakway) == False:
        print('Ошибка. Пробуем еще раз. При использовании Flatpak-версии пример корректного пути:')
        print('/home/username/.var/app/io.github.alainm23.planify/data/io.github.alainm23.planify/database.db')
        ans_askway()
    else:
        pass

def ans_confirmway(otvet):
    if otvet == 'Y' or otvet == 'y':
        #продолжение алгоритма
        pass
    elif otvet == 'N' or otvet == 'n':
        ans_askway()
    else:
        ans_confirmway()

class KhAddEntrys_in_Projects(Base):
    __tablename__ = 'Projects'

    id = Column(String, primary_key=True)
    name = Column(String)
    inbox_project = Column(Integer) # =0 массово ставить
    is_deleted = Column(Integer) # =0 массово ставить
    is_archived = Column(Integer) # =0 массово ставить
    parent_id = Column(String) # тут указываю ID родителя проекта
    source_id = Column(String)
    

class KhAddEntrys_in_Items(Base):
   __tablename__ = 'Items'
   
   id = Column(String, primary_key=True)
   content = Column(String)
   description = Column(String)
   due = Column(String)
   added_at = Column(String)
   completed_at = Column(String)
   updated_at = Column(String)#
   section_id = Column(String)#
   project_id = Column(String)
   parent_id = Column(String)
   priority = Column(Integer)#
   child_order = Column(Integer)#
   checked = Column(Integer)#
   is_deleted = Column(Integer)#


#для поиска ключа по значению
def get_key(projects_dict, value):
    for k, v in projects_dict.items():
        if v == value:
            return k

#Теперь надо создать проекты из полученного `projects_dict`
def create_projects_from_projects_dict(projects_dict):
    
    for i in projects_dict.values():

        if (i[0] == '') and (i[1] != ''):
            rowname = i[1]
        elif (i[1] == '') and (i[0] != ''):
            rowname = i[0]
        elif (i[0] != '') and (i[1] != ''):
            rowname = i[1]
        else:
            rowname = 'ProjectNameError'
        
        kh_write_row = KhAddEntrys_in_Projects (
            id = get_key(projects_dict, i),
            name = rowname,
            inbox_project = 0,
            is_deleted = 0,
            is_archived = 0,
            parent_id = '',
            source_id = 'local'
            )
        session.add(kh_write_row)
    session.commit()



def csvdate_to_stringdate(csvd):
    empty_str = ""
    try:
        parseddate = parser.parse(csvd)
        return str(parseddate.date())
    except Exception:
        return empty_str

def add_entrys_to_database():
    for i in range(len(data_list)):
        if len(data_list[i]) > 2 and (data_list[i][0] != 'Folder Name'):
            if (data_list[i][8]) == '':
                checked_value = 0
            else:
                checked_value = 1
            kh_write_row = KhAddEntrys_in_Items(id = 'import' + str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '-item-' + (data_list[i][22]),
                content = (data_list[i][2]),
                description = (data_list[i][5]),
                due = r'{"date":"' + csvdate_to_stringdate(data_list[i][8]) + r'","timezone":"","is_recurring":false,"recurrency_type":"6","recurrency_interval":"0","recurrency_weeks":"","recurrency_count":"0","recurrency_end":""}',
                added_at = (data_list[i][13]),
                completed_at = (data_list[i][14]),
                section_id = '',
                project_id = get_key(projects_dict, [data_list[i][0], data_list[i][1]]),
                parent_id = (data_list[i][23]),
                checked = checked_value,
                is_deleted = 0
            )
            session.add(kh_write_row)
    session.commit()


###
###
###

#старт интерактива
ans_start()

#открытие *.csv
with open('1.csv') as file:
    data_list = [row for row in csv.reader(file)]
print(len(data_list))

#пробую искать пары папка-проект:
projects_set = set()
projects_dict = dict()

for i in range (len(data_list)):
    if len(data_list[i]) > 2 and (data_list[i][0] != 'Folder Name'):
        projects_set.add(data_list[i][0] + '$,$' + data_list[i][1])
    else:
        pass

#дозаписываю в словарь id проектов, которые будут созданы: v2
for i in range (len(projects_set)):
    i_value = projects_set.pop()
    projects_dict[str(datetime.now().date()) + '_project_' + str(i+1)] = [i_value.split('$,$')[0], i_value.split('$,$')[1]]

#создаю проекты  в database.db
create_projects_from_projects_dict(projects_dict)

#добавляю задачи в database.db
add_entrys_to_database()