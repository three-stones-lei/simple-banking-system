import random
import sqlite3
# Write your code here
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS card (         
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      number TEXT,
      pin TEXT,
      balance INTEGER DEFAULT 0
      );
  """)
conn.commit()

# Luhn algorithm check
def check_luhn_algorithm(card_number):
    add_all_number = 0
    for i in range(15):
            if i % 2 == 0:
                current_number = int(card_number[i]) * 2
            else:
                current_number = int(card_number[i])
            if current_number > 9:
                current_number -= 9
            add_all_number += current_number
    calculate_number = int(str(add_all_number)[-1])
    if calculate_number != 0:
        check = 10 - int(str(add_all_number)[-1])
    else:
        check = 0
    if check == int(card_number[15]):
        return True
    else:
        return False

# card_number_pin = {}
while True:
    break_flag = False
    print('''1. Create an account
2. Log into account
0. Exit''')
    choose_number = int(input())
    if choose_number == 1:
        print()
        card_number = ""
        password = ""
        check = 0
        add_all_number = 0
        for i in range(9):
            card_number += str(random.randint(1, 9))
        card_number = '400000' + card_number
        for i in range(15):
            if i % 2 == 0:
                current_number = int(card_number[i]) * 2
            else:
                current_number = int(card_number[i])
            if current_number > 9:
                current_number -= 9
            add_all_number += current_number
        calculate_number = int(str(add_all_number)[-1])
        if calculate_number != 0:
            check = 10 - int(str(add_all_number)[-1])
        else:
            check = 0
        card_number += str(check)
        for i in range(4):
            password += str(random.randint(0, 9))
      # card_number_pin[card_number] = password
        cur.execute(f'''INSERT INTO card 
        (number, pin, balance)
        VALUES({card_number},{password},0);
        ''')
        conn.commit()
        print('Your card has been created')
        print('Your card number:')
        print('{}'.format(card_number))
        print('Your card PIN:')
        print ('{}'.format(password))
        print()
        continue
    elif choose_number == 2:
        print()
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin = input()
      # is_right = 0
        cur.execute(f'SELECT * FROM card WHERE number={card_number} and pin={pin};')
      #  for i in card_number_pin:
      #      if (card_number == i) and (card_number_pin[i] == pin):
      #          is_right = 1
      #          break
      #      else:
      #          is_right = 0
        if len(cur.fetchall()) != 0:
            print()
            print('You have successfully logged in!')
            print()
            while True:
                print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
                number = int(input())
                if number == 1:
                    cur.execute(f'SELECT balance FROM card WHERE number = {card_number}')
                    print()
                    print(f'Balance: {cur.fetchone()}')
                    print()
                    continue
                elif number == 2:
                    print()
                    print('Enter income:')
                    cur.execute(f'UPDATE card SET balance = balance + {int(input())} WHERE number = {card_number}')
                    conn.commit()
                    print('Income was added!')
                    print()
                elif number == 3:
                    print()
                    print('Transfer')
                    print('Enter card number:')
                    destination_card_number = input()
                    cur.execute(f'SELECT balance FROM card WHERE number = {destination_card_number}')
                    if not check_luhn_algorithm(destination_card_number):
                        print('Probably you made mistake in the card number.')
                        print('Please try again!')
                        print()
                        continue
                    if len(cur.fetchall()) == 0:
                        print('Such a card does not exist.')
                        print()
                        continue


                    print('Enter how much money you want to transfer:')
                    transfer_number = int(input())
                    cur.execute(f'SELECT balance FROM card WHERE number = {card_number}')
                    original_balance = cur.fetchone()[0]
                    if transfer_number > original_balance:
                        print('Not enough money!')
                        print()
                        continue
                    cur.execute(f'UPDATE card SET balance = balance - {transfer_number} WHERE number = {card_number}')
                    conn.commit()
                    cur.execute(f'UPDATE card SET balance = balance + {transfer_number} WHERE number = {destination_card_number}')
                    conn.commit()
                    print('Success!')
                    print()

                elif number == 4:
                    print()
                    cur.execute(f'DELETE FROM card WHERE number = {card_number}')
                    conn.commit()
                    print('The account has been closed!')
                    print()
                    break

                elif number == 5:
                    print()
                    print('You have successfully logged out!')
                    print()
                    break
                elif number == 0:
                    print()
                    break_flag = True
                    break
        else:
            print()
            print('Wrong card number or PIN!')
            print()
            continue
    elif choose_number == 0:
        print()
        print('Bye!')
        break

    if break_flag == True:
        conn.close()
        break


