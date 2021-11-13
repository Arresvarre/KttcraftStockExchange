import mysql.connector
import os



def databse_function(func):
    def wrapper(*args, **kwargs):
        mydb = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_DB"))
        mycursor = mydb.cursor()
        result = func(*args, **kwargs, mycursor=mycursor, mydb=mydb)
        mydb.disconnect()
        return result
    return wrapper


# user related:
@databse_function
def staff_perm(discordId, mycursor=None, mydb=None):
    mycursor.execute(f'''
        SELECT staff
        FROM user
        WHERE discordId = {discordId}
    ''')
    result = mycursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False


@databse_function
def addPrice_perm(discordId, mycursor=None, mydb=None):
    mycursor.execute(f'''
        SELECT addPrice
        FROM user
        WHERE discordId = {discordId}
    ''')
    result = mycursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False


@databse_function
def get_from_user(discordId, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT *
            FROM user
            WHERE discordId = {discordId};
            ''')
    result = mycursor.fetchall()
    return result[0]

@databse_function
def get_from_user_id(user_id, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT *
            FROM user
            WHERE id = {user_id};
            ''')
    result = mycursor.fetchall()
    return result[0]

@databse_function
def user_in_database(discordId, mycursor=None, mydb=None):
    mycursor.execute(f'''
        SELECT COUNT(1)
        FROM user
        WHERE discordId = {discordId};
        ''')
    result = mycursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False

@databse_function
def uuid_in_database(uuid, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT COUNT(1)
            FROM user
            WHERE uuid = '{uuid}';
            ''')
    result = mycursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False

@databse_function
def update_addPrice_permission(DiscordId, mycursor=None, mydb=None):
    if not addPrice_perm(DiscordId):
        mycursor.execute(f'''
            UPDATE user
            SET addPrice = 1
            WHERE discordId = {DiscordId}
            ''')
        mydb.commit()
        return True
    else:
        mycursor.execute(f'''
            UPDATE user
            SET addPrice = 0
            WHERE discordId = {DiscordId}
            ''')
        mydb.commit()
        return False

@databse_function
def update_staff_permission(DiscordId, mycursor=None, mydb=None):
    if not staff_perm(DiscordId):
        mycursor.execute(f'''
            UPDATE user
            SET staff = 1
            WHERE discordId = {DiscordId}
            ''')
        mydb.commit()
        return True
    else:
        mycursor.execute(f'''
            UPDATE user
            SET staff = 0
            WHERE discordId = {DiscordId}
            ''')
        mydb.commit()
        return False

@databse_function
def add_user_to_database(discordId, addedById, uuid, mycursor=None, mydb=None):
    mycursor.execute(f'''
        INSERT INTO user(discordId, uuid, addedBy)
        Values({discordId}, '{uuid}', {addedById})
        ''')
    mydb.commit()

@databse_function
def update_user_stock(userId, ticker, quantity, mycursor=None, mydb=None):
    mycursor.execute(f'''
        INSERT INTO user_stock 
        VALUES({userId}, '{ticker}', {quantity})
        ON DUPLICATE KEY UPDATE quantity={quantity};
        ''')
    mydb.commit()

@databse_function
def get_user_stock(user, mycursor=None, mydb=None):
    mycursor.execute(f'''
        SELECT quantity, ticker
        FROM user_stock
        WHERE user = {user}
        ''')
    result = mycursor.fetchall()
    return result



# company related:
@databse_function
def update_price(ticker, user, price, mycursor=None, mydb=None):
    mycursor.execute(f'''
        INSERT INTO price(company, user, price)
        VALUES("{ticker}", {user}, {price});
        ''')
    mydb.commit()


@databse_function
def company_in_database(ticker, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT COUNT(1)
            FROM company
            WHERE ticker = '{ticker}';
            ''')
    result = mycursor.fetchone()
    if result[0] == 1:
        return True
    else:
        return False


@databse_function
def get_from_company(ticker, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT *
            FROM company
            WHERE ticker = '{ticker}';
            ''')
    result = mycursor.fetchall()
    return result[0]


@databse_function
def get_from_board(ticker, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT *
            FROM board
            WHERE ticker = '{ticker}';
            ''')
    result = mycursor.fetchall()
    return result


@databse_function
def get_price(ticker, mycursor=None, mydb=None):
    mycursor.execute(f'''
            SELECT price, time
            FROM price
            WHERE company = "{ticker}"
            ''')
    result = mycursor.fetchall()
    return result