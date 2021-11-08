from ksedb import *
import mc


user = ''
ticker = ''
price = 0
quantity = 0


not_staff_permission = 'Du har inte peronalbehörighet.'

not_addprice_permission = 'Du har inte behörighet att ändra aktiers pris'
user_not_in_database = 'Spelaren finns inte i databasen.'


updated_addPrice_true = 'Gav spelare behörighet för ändra pris.'
updated_addPrice_false = 'Tog bort behörighet för spelare att ändra pris.'
update_staff_true = 'Gav spelare personalbehörighet.'
update_staff_false = 'Tog bort bersonalbehörighet från spelare.'
company_not_in_database = 'Företaget finns inte i databasen.'
updated_stock_price = 'Updaterade aktiens pris'
user_stock_updated = 'Updaterade spelares aktieinnehav'


red_color = 0x00d9ff


def add_user(discordId,uuid, addedby_discordId):
    if staff_perm(addedby_discordId):
        print(user_in_database(discordId))
        print(uuid_in_database(uuid))
        if not user_in_database(discordId) and not uuid_in_database(uuid):
            dbId = get_from_user(addedby_discordId)[0]
            print(discordId, dbId, uuid)
            add_user_to_database(discordId, dbId, uuid)
            return True, f'Lade till {mc.UUID_to_mc_name(uuid)} i databasen.'
        else:
            return False, f'{mc.UUID_to_mc_name(get_from_user(discordId)[6])} finns redan i databsasen.'
    else:
        return False, f'Du har inte peronalbehörighet.'


def update_addPrice(discordId, addedby_discordId):
    if staff_perm(addedby_discordId):
        if user_in_database(discordId):
            if update_addPrice_permission(discordId):
                return updated_addPrice_true
            else:
                return updated_addPrice_false
        else:
            return user_not_in_database
    else:
        return not_staff_permission


def update_staff(discordId, addedby_discordId):
    if staff_perm(addedby_discordId):
        if user_in_database(discordId):
            if update_staff_permission(discordId):
                return update_staff_true
            else:
                return update_staff_false
        else:
            return user_not_in_database
    else:
        return not_staff_permission


def update_stock_price(ticker, discordId, price):
    if addPrice_perm(discordId):
        if company_in_database(ticker):
            update_price(ticker, get_from_user(discordId)[0], price)
            return updated_stock_price
        else:
            return company_not_in_database
    else:
        return not_addprice_permission


def user_stock(discordId, ticker, quantity, addedby_discordId):
    if staff_perm(addedby_discordId):
        if user_in_database(discordId):
            if company_in_database(ticker):
                update_user_stock(get_from_user(discordId)[0], ticker, quantity)
                return user_stock_updated
            else:
                return company_not_in_database
        else:
            return user_not_in_database
    else:
        return not_staff_permission