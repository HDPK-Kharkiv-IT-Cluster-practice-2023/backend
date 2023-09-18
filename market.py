"""
Модули для управления магазином и покупкой предметов персонажем.
"""

from random import shuffle
from typing import Union

character_template = {
    'Health': 0,
    'Attack': 0,
    'Defence': 0,
    'Luck': 0
}
character_info = {
    'Level': 1,
    'Experience': 0,
    'Money': 100,
    'Fullname': ''
}

marketing_goods = [
    {
        'Title': 'Thief finger',
        'Attack': 1,
        'Price': 20
    },
    {
        'Title': 'Sword of Fire',
        'Attack': 2,
        'Price': 50
    },
    {
        'Title': 'Shield of Honor',
        'Defence': 3,
        'Price': 80
    },
    {
        'Title': 'Hawk head',
        'Defence': 2,
        'Price': 30
    },
    {
        'Title': "Paladin's blessing",
        'Luck': 2,
        'Price': 30
    },
    {
        'Title': 'BCAA',
        'Health': 3,
        'Price': 50
    }
]

shuffle(marketing_goods)


def market(p):
    """
    Функция для совершения покупки предмета в магазине.

    Args:
        p (dict): Словарь с информацией о персонаже.

    Returns:
        dict: Обновленный словарь с информацией о персонаже после покупки.
    """
    p_stats = p.get('Stats').copy()
    print(p)
    priority = min(p_stats, key=p_stats.get)

    for id, good in enumerate(marketing_goods):
        if good.get(priority) and good.get('Price') <= p.get('Money'):
            print("Вы купили {good['Title']} за {good['Price']} монет.")
            p['Money'] -= good.get('Price')
            p['Stats'][priority] += good.get(priority)
            del marketing_goods[id]
            p['thing'] = good.get('Title')
            break
    return p


p1 = character_info.copy()
p1['Fullname'] = "Имя персонажа"  
p1['Stats'] = character_template.copy()
p1['Stats']['Health'] = 10  
p1['Money'] = 100  


market(p1)

print(p1)
