from shop import Shop
from ssh_tunnel import create_ssh_tunnel


def main():
    char_id = 2  # Replace with the desired character ID

    tunnel = create_ssh_tunnel()
    tunnel.start()

    shop_instance = Shop(0, char_id, tunnel)

    while True:
        print("What do you want to buy?")
        print("1. Weapons")
        print("2. Items")
        print("3. Legendary Items")
        print("0. Exit")
        sub_choice = input("Enter the category number you want to view, or 0 to exit: ")

        if sub_choice == "0":
            break
        elif sub_choice == "1":
            shop_instance.show_weapons()
        elif sub_choice == "2":
            shop_instance.show_items()
        elif sub_choice == "3":
            shop_instance.show_legendary_items()

        try:
            choice = int(input('Enter the item number you want to buy, or 0 to exit: '))
            if choice == 0:
                break

            if sub_choice == "1":
                items = {**shop_instance.melee_weapons, **shop_instance.ranged_weapons}
            elif sub_choice == "2":
                items = {**shop_instance.items}
            elif sub_choice == "3":
                items = {**shop_instance.legendary_items}
            else:
                raise ValueError

            if choice > len(items) or choice < 1:
                raise ValueError

            item_name = list(items.keys())[choice - 1]
            item_price = items[item_name]['price']
            if shop_instance.purchase_item(item_name, item_price):
                print(f'You bought {item_name} for {item_price} UAH. Remaining balance: {shop_instance.money} UAH')
            else:
                print('Failed to purchase the item. Insufficient funds.')

        except ValueError:
            print('Invalid input. Please enter a valid number or 0 to exit.')


if __name__ == "__main__":
    main()
