# Фитнес-трекера

**Фитнес-трекера** - программа, которая на основе поступивших данных формирует статистику тренировки.

## Функционал фитнес-трекера:
- рассчитывает дистанцию в км
- рассчитывает среднюю скорость движения в км/ч
- рассчитывает количество затраченных калорий

## Виды тренировок:
- бег
- спортивная ходьба
- плавание

## Запуск проекта:
- клонировать репозиторий
- установить виртуальное окружение командой: python -m venv venv
- активировать виртуальное окружение
- установить зависимости из файла requirements.txt
- запустить фитнес-трекер командой: python test_homework.py 

## Пример входных данных:
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

## Пример выходных данных:
    Тип тренировки: Swimming; Длительность: 1.000 ч.; Дистанция: 0.994 км; Ср. скорость: 1.000 км/ч; Потрачено ккал: 336.000.
    Тип тренировки: Running; Длительность: 1.000 ч.; Дистанция: 9.750 км; Ср. скорость: 9.750 км/ч; Потрачено ккал: 797.805.
    Тип тренировки: SportsWalking; Длительность: 1.000 ч.; Дистанция: 5.850 км; Ср. скорость: 5.850 км/ч; Потрачено ккал: 349.252.

## Стэк технологии
- Python: 3.11

Подробнее с используемыми зависимостями вы можете ознакомиться в файле requirements.txt

## Об авторе проекта
Барабанщиков Кирилл, я python backend разработчик.

## Мои контакты
- Telegram: https://t.me/Kirill_Barabanshchikov
- почта: bks2408@mail.ru
