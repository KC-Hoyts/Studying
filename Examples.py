import time

print('Добро пожаловать в игру Крестики-Нолики!\nВведите имена игроков:')
a=input('Игрок №1 (ставит "x" и ходит первым): ')
b=input('Игрок №2 (ставит "o" и ходит вторым): ')
print(f'\n{a} и {b}! По ходу игры вводите номер строки и колонки для того, чтобы поставить "х" или "о" (английская раскладка).')
print('\nИгровое поле выглядит вот так:')
field=[
       {'st1': ' ', 'st2':'0', 'st3':'1', 'st4':'2'},
       {'no' : '0', '00':'-', '01':'-', '02':'-'},
       {'no' : '1', '10':'-', '11':'-', '12':'-'},
       {'no' : '2', '20':'-', '21':'-', '22':'-'}]

currently_player=a #Текущий игрок (Необходим для отображения текущего игрока)

def show_field():
    for row in field:
        for colomn in row.values():
            print(colomn, end=' ')
        print()

show_field()
print('Приятной игры!')
input('\n-----------------------------\nНажмите Enter для начала игры\n-----------------------------')
time_start=time.time()
def game():
    global field
    global currently_player
    result_a=set()
    result_b=set()
    while '-' in str(list(map(str, field))):

        step=input(f'\nВаш ход, {currently_player}. Введите координаты хода:')
        for row in field:
            if 'st1' in row.keys():
                pass
            else:
                if step in row.keys():
                    if row[step]!='-':
                        print('(!) Клетка уже занята! Выберите другую клетку!')
                    elif currently_player==a:
                        row[step]='x'
                        currently_player = b
                        result_a.add(step)

                    else:
                        row[step] = 'o'
                        currently_player = a
                        result_b.add(row[step])
        show_field()
        if check_winner(result_a or result_b):
            time_finish = time.time()
            print(f"Победитель - {a if result_a else b}!\n")
            print('Время игры заняло %2.2f минут'% ((time_finish-time_start)/60))
            print('\n==================================================\n')
            print('Надеемся Вам понравилось тестировать нашу разработку. Спасибо! :)')
            print('\nSkillFactory, FPW-097, \nЖернаков Кирилл Сергеевич,\nИтоговое задание по Python, \n26.11.2023')
            break
    else:
        print('\n(!) Упс! Похоже, поля закончились. Победила дружба! ^_^')


def check_winner(*args):
    combinations = [{'00', '10', '20'}, {'01', '11', '21'}, {'02', '12', '22'}, {'00', '01', '02'},
         {'10', '11', '12'}, {'20', '21', '22'}, {'00', '11', '22'}, {'02', '11', '20'}]
    final_result=False
    for ch in combinations:
        if ch in args:
            print('\n--------------------------------------------------'
                  '\n(!) === СТОП ИГРА! У нас есть Победитель! === (!)'
                  '\n--------------------------------------------------')
            final_result=True
    return final_result


game()

