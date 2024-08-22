Скрипт для импорта задач из TickTick в приложение [Planify](https://github.com/alainm23/planify).

1. Идем в [TickTick](https://ticktick.com/webapp/), экспортируем свои задачи в *.csv-файл.
2. Переименовываем полученный *.csv-файл в `1.csv` и кладем в ту же директорию, куда скачали `ticktick_to_planify.py`.
3. Запускаем `ticktick_to_planify.py` и следуем инструкциям.


P.S.
Здесь файл 1.csv просто для примера.
Не забудьте сделать резервную копию *.db-файла используемой базы данных Planify. В случае использования Flatpak-версии, база данных будет лежать по пути `/home/USERNAME/.var/app/io.github.alainm23.planify/data/io.github.alainm23.planify/`
