import sqlite3
import os

# database name:
dbname = "appdata"
MAX_CARD_VALUE = 9999
MIN_CARD_VALUE = 0
# create database file if not exist:
database = sqlite3.connect(database=f"{os.path.join(os.getcwd(), dbname)}")
cursor = database.cursor()
# create the table if it does not exist:
create_table = '''CREATE TABLE IF NOT EXISTS users
                (card_no TEXT,
                contract TEXT,
                wallet INT,
                PRIMARY KEY (card_no));'''
cursor.execute(create_table)
database.commit()


# create new card no data
def new_card():
    last_index = '''SELECT COUNT(*)
                    FROM users'''
    nu = cursor.execute(last_index).fetchone()[0]
    if nu > MAX_CARD_VALUE:
        print("cannot create more cards")
        exit()
    if nu < 10:
        card = '000' + str(nu)
    elif nu < 100:
        card = '00' + str(nu)
    elif nu < 1000:
        card = '0' + str(nu)
    add = '''INSERT INTO users
                    (card_no,contract,wallet)
                    VALUES (?, ?, ?);'''
    cursor.execute(add, (card, "None", 0))
    database.commit()
    return card


# used to add a card or update plan/wallet for the card_no
def add_update_card(card, cont, wallet):
    arr = ['North', 'South', 'Center', 'None']
    contract_exists = False
    try:
        num = int(card)
    except ValueError:
        return "error card value is not valid"
    if num < MIN_CARD_VALUE or num > MAX_CARD_VALUE:
        return "error card value is not valid"
    if get_exists(card) == 'no':
        return 'card does not exist in the database'
    for c in arr:
        if cont == c:
            contract_exists = True
    if contract_exists:
        try:
            int(wallet)
        except ValueError:
            return 'error wallet value is not a number'
        add = '''INSERT OR REPLACE INTO users
                (card_no,contract,wallet)
                VALUES (?, ?, ?);'''
        cursor.execute(add, (card, cont, wallet))
        database.commit()
        return 'updated'
    return 'error contract value does not exist'


# gives all the card info
def get_card_info(card):
    select_card = f'''SELECT *
                    FROM users
                    WHERE card_no="{card}";'''
    cursor.execute(select_card)
    card_info = cursor.fetchone()
    return str(f"{card_info[0]},{card_info[1]},{card_info[2]}")


# check if card exists
def get_exists(card):
    try:
        c = int(card)
        if c < MIN_CARD_VALUE or c > MAX_CARD_VALUE:
            print("no")
            return 'No'
        else:
            select_card = f'''SELECT *
                            FROM users
                            WHERE (card_no="{card}");'''
            cursor.execute(select_card)
            card_info = cursor.fetchone()
            if card_info:
                return 'yes'
            return 'no'
    except ValueError:
        return 'no'


# give all card_no
def get_all_cards():
    # getting the col card_no
    select_everything = '''SELECT card_no
                        FROM users;'''
    cursor.execute(select_everything)
    # pu the results into a list
    results = cursor.fetchall()
    # reverse the results to get card numbers in order when pop them to new list
    results.reverse()
    try:
        card = results.pop()[0]
        make_str = str(card)
        while results:
            load = str(results.pop()[0])
            make_str = make_str + "," + str(load)
        return make_str
    except IndexError:
        print('err')
    return "No cards exist"


# close db app done running
def end():
    cursor.close()
    database.close()
