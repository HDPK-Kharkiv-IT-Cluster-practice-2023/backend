from random import randint, choice, shuffle
from faker import Faker

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

knife = {
    'Title': 'Thief finger',
    'Attack': 1,
    'Price': 20
}

sword = {
    'Title': 'Sword of Fire',
    'Attack': 2,
    'Price': 50
}

shield = {
    'Title': 'Shield of Honor',
    'Defence': 3,
    'Price': 80
}

helmet = {
    'Title': 'Hawk head',
    'Defence': 2,
    'Price': 30
}

blessing = {
    'Title': 'Palladin\'s blessing',
    'Luck': 2,
    'Price': 30   
}

sportpit = {
    'Title': 'BCAA',
    'Health': 3,
    'Price': 50   
}


marketing_goods = [knife, sword, shield, helmet, blessing, sportpit]
shuffle(marketing_goods)

fake = Faker()
score = 25


def create_player(score=score):
    new_score = score
    new_character = character_template.copy()
    new_character['Luck'] = randint(0, 10)
    new_score -= new_character['Luck']

    while new_score > 0:
        key = choice(list(new_character.keys()))

        if key == 'Luck':
            continue

        new_score -= 1
        new_character[key] += 1

    return new_character

def hit(p1, p2):
    attack_points = p1.get('Stats').get('Attack')
    print(attack_points)

    if randint(0, 100) <= p1.get('Stats').get('Luck'):
        attack_points *= 2
        print('Critical hit')
    if randint(0, 100) <= p2.get('Stats').get('Luck'):
        attack_points = 0
        print('Dodge')
    if attack_points > 0:
        defence_points = p2.get('Stats').get('Defence')
        health_points = p2.get('Stats').get('Health')
        attack_points -= min(defence_points, attack_points)
        health_points -= attack_points
        print('Health is', health_points)
        if health_points <= 0:
            print('Death')
        p2['Stats']['Health'] = health_points
    return p2

def market(p):
    p_stats = p.get('Stats').copy()
    print(p)
    priority = min(p_stats, key = p_stats.get)
    print(priority)

    for id, good in enumerate(marketing_goods):
        if good.get(priority) and good.get('Price') < p.get('Money'):
            print(good, end='\n')
            p['Money'] -= good.get('Price')
            p['Stats'][priority] += good.get(priority)
            del marketing_goods[id]
            p['thing'] = good.get('Title')
            break
    return p

p1 = character_info.copy()
p1['Fullname'] = fake.name()
p1['Stats'] = create_player()

p2 = character_info.copy()
p2['Fullname'] = fake.name()
p2['Stats'] = create_player()

# print(p1, p2, sep='\n')

market(p1)
market(p2)

print(p1, p2, sep='\n')


while True:
    if p1.get('Stats').get('Health') > 0:
        hit(p1,p2)
        print(p1, p2, sep='\n')
    else:
        print(p1.get('Fullname'), ' is dead')
        break
    if p2.get('Stats').get('Health') > 0:
        hit(p2, p1)
        print(p1, p2, sep='\n')
    else:
        print(p2.get('Fullname'), ' is dead')
        break

