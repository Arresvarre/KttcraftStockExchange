import os

from discord import *
from discord.ext import commands


intents = Intents.default()
intents.members = True
intents.messages = True

command_channel_ids = (822020156065579032, 905425177557483562)
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

bot = commands.Bot(command_prefix=".", intents=intents, case_insensitive=True)

from dbfunc import *
from mc import *
from ksedb import *


def prefix(number):
    if number < 1000:
        return number, ""
    elif number < 1000000:
        return round(number/1000), "k"
    else:
        return round(number/1000000), "M"


def log_channel():
    id = os.getenv("LOG_ID")
    return bot.get_channel(int(id))


def embed_message(author, cause, text, thumbnail=None, color=0x00d9ff, footer=None):
    embed = Embed(title=cause, description=text, color=color)
    embed.set_author(name=author)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if footer:
        embed.set_footer(text=footer)
    return embed


async def command_in_command_channel(ctx):
    import json
    env_list = json.loads(os.environ['COMMAND_CHANNELS'])
    if ctx.channel.id in env_list:
        return True
    else:
        await ctx.message.delete()
        return False


@bot.event
async def on_ready():
    #await log_channel().send(embed=embed_message('KSE LOG', 'Ansluten', '', color=0x7FFF00))
    pass


@bot.event
async def on_member_join(m):
    await log_channel().send(embed=embed_message('KSE LOG', f'{m.name} har gått med',f'ID:{m.id}',thumbnail=str(m.avatar_url)))


@bot.event
async def on_member_remove(m):
    await log_channel().send(embed=embed_message('KSE LOG', f'{m.name} har lämnat',f'ID:{m.id}',thumbnail=str(m.avatar_url)))


@bot.event
async def on_message_edit(m, m2):
    if not m.author == bot.user:
        await log_channel().send(embed=embed_message('KSE LOG', f'{m.author.name} har ändrat ett meddelande',f'Innan:\n {m.content}\nEfter:\n {m2.content}', thumbnail=m.author.avatar_url, footer=f'MessageID: {m.id}'))


@bot.event
async def on_message_delete(m):
    if not m.author == bot.user:
        await log_channel().send(embed=embed_message('KSE LOG', f'{m.author.name} har raderat ett meddelande',f'Meddelande:\n {m.content}', thumbnail=m.author.avatar_url, footer=f'MessageID: {m.id}'))


@bot.command(aliases=['u'])
async def user(ctx, user = None, mc_name = None):
    nu = False
    inDatabase = False
    if user == None:
        user = get_from_user(ctx.author.id)
        if user_in_database(ctx.author.id):
            inDatabase = True
    else:
        try:
            user = ctx.guild.get_member(int(user.strip('<@!>')))
            if user_in_database(user.id):
                inDatabase = True
                user = get_from_user(user.id)
            else:
                user = user.id
        except Exception as e:
            if valid_mc_name(user):
                nu = True
                if uuid_in_database(mc_name_to_UUID(user)):
                    inDatabase = True
                    user = get_from_user_uuid(mc_name_to_UUID(user))

    e = ''
    if await command_in_command_channel(ctx):
        if mc_name == None:
            if inDatabase:
                e = embed_message('KSE Bot', UUID_to_mc_name(user[6]),
                                  f'-INFO-\n'
                                  f'UUID : {user[6]}\n'
                                  f'DiscordId : {user[1]}\n'
                                  f'Behörighet : {"Personal behörighet" if user[5] else ""}{"Ändra pris behörighet" if user [4] and not user[5] else ""}{"Inga" if not user[4] and not user[5] else ""}\n'
                                  f'Tillagd : {user[2]} av {UUID_to_mc_name(get_from_user_id(user[3])[6])}',
                                  thumbnail=mc.mc_head(user[6]))
            else:
                raise commands.MemberNotFound('Not found player')
        else:

            print(user)

            a = [False, "ERROR"]
            if mc_name == "NU" and nu:
                a = add_non_user(mc_name_to_UUID(user), ctx.author.id)
                uuid = mc_name_to_UUID(user)
            if not nu and valid_mc_name(mc_name):
                uuid = mc_name_to_UUID(mc_name)
                a = add_user(user, uuid, ctx.author.id)
            if a[0]:
                await update_names(ctx)
                e = embed_message('KSE Bot', 'Lade till seplare i databas', a[1], color=0x7FFF00, thumbnail=mc.mc_head(uuid))
            else:
                e = embed_message('KSE Bot', 'Error', a[1], color=0xDC143C)

        await ctx.send(embed=e)



@user.error
async def user_error(ctx, error):
    e = ''
    if await command_in_command_channel(ctx):
        print(error)
        if isinstance(error, commands.MemberNotFound):
            e = embed_message('KSE Bot', 'Error', 'Hittade inte spelare.', color=0xDC143C)
        elif isinstance(error, commands.errors.CommandInvokeError) or isinstance(error, commands.MissingRequiredArgument):
            e = embed_message('KSE Bot', 'Error', '.user user mc_name', color=0xDC143C)
        await ctx.send(embed=e)


@bot.command(aliases=['p'])
async def price(ctx, ticker, price=None):
    e = ''
    sende = True
    if await command_in_command_channel(ctx):
        if company_in_database(ticker):
            c = get_from_company(ticker)
            if price is None:
                price = get_price(ticker)
                e = embed_message('KSE Bot', f'Pris för {c[0]}', str(price[-1][0]) + " mm", thumbnail=c[5])
            elif price is not None:
                u = update_stock_price(ticker, ctx.author.id, price)
                if u:
                    e = embed_message('KSE Bot', f'Uppdaterat pris för {c[0]}', price + ' mm', thumbnail=c[5], color=0x7FFF00)
                    await utils.get(ctx.guild.channels, id=int(c[8])).send(embed=e)
                    sende = False
        else:
            e = embed_message('KSE Bot', 'Error', f'{ticker.upper()} finns inte i databasen', color=0xDC143C)
    if sende:
        await ctx.send(embed=e)


@price.error
async def price_error(ctx, error):
    e = ''
    if await command_in_command_channel(ctx):
        print(error)
        if isinstance(error, commands.errors.CommandInvokeError):
            e = embed_message('KSE Bot', 'Error', '.price ticker (price) \n Exempel: \n .price MACO (1000)',color=0xDC143C)
        await ctx.send(embed=e)


@bot.command(aliases=['c'])
async def company(ctx, ticker, subc=None, q=None):
    e=''
    if await command_in_command_channel(ctx):
        if company_in_database(ticker):
            c = get_from_company(ticker)
            if subc is None:

                e = embed_message('KSE Bot', f'Info om {c[0]}', f'Kortnamn: {c[1]}\nGrundare: {UUID_to_mc_name(get_from_user_id(c[3])[6])}\nAntal aktier: {c[9]}st\nTillagd: {c[2]} av {UUID_to_mc_name(get_from_user_id(c[4])[6])}', thumbnail=c[5])
            else:
                if subc == "board":
                    board = []
                    for b in get_from_board(ticker):
                        if b[2]:
                            board.insert(0, (b[0], True))
                        else:
                            board.append((b[0], False))
                    m =''
                    for i in board:
                        if i[1]:
                            m += f'{UUID_to_mc_name(get_from_user_id(i[0])[6])} (VD)\n'
                        else:
                            m += f"{UUID_to_mc_name(get_from_user_id(i[0])[6])}\n"
                    e = embed_message('KSE Bot', f'{c[0]}s styrelse', m, thumbnail=c[5])
                elif subc == "shareholders":
                    if company_in_database(ticker):
                        shareholders = []
                        m = ''
                        ci = get_from_company(ticker)
                        for i in get_shareholders(ticker):
                            shareholders.append(i)

                        def sort_shareholders(obj):
                            return obj[1]
                        shareholders.sort(key=sort_shareholders)
                        shareholders.reverse()
                        for i in shareholders:
                            if i[1]:
                                m += f'{UUID_to_mc_name(get_from_user_id(i[0])[6])} : {i[1]}\n'
                        try:
                            if ci[10] is not None:
                                m2 = f"{ci[1]} : {ci[10]}\n" + m
                            else:
                                m2 = f"{ci[1]} : 0\n" + m
                        except UnboundLocalError:
                            m2 = f"{ci[1]} : 0\n" + m
                        e = embed_message('KSE Bot', f'{c[0]}s aktieägare', m2, thumbnail=c[5])
                    else:
                        e = embed_message('KSE Bot', 'Error', f'{ticker.upper()} finns inte i databasen', color=0xDC143C)
                elif subc == "stocks":

                    if company_stock(ctx.author.id, ticker, q):
                        e = embed_message('KSE Bot', f'Uppdaterat antal aktier för {ticker.upper()}', q + " st", thumbnail=c[5],
                                          color=0x7FFF00)
                    else:
                        e = embed_message('KSE Bot', 'Error', company_stock(ctx.author.id, ticker, q)[1], color=0xDC143C)
                elif subc == "count":
                    if company_in_database(ticker):
                        count = 0
                        for i in get_shareholders(ticker):
                            count += i[1]
                        if get_from_company(ticker)[10]:
                            count += get_from_company(ticker)[10]
                        e = embed_message('KSE Bot', 'Antal aktier i databasen', f'{count} st \n{get_from_company(ticker)[9]-count} Saknas', thumbnail=get_from_company(ticker)[5])
                    else:
                        e = embed_message('KSE Bot', 'Error', f'{ticker.upper()} finns inte i databasen',color=0xDC143C)
        else:
            e = embed_message('KSE Bot', 'Error', f'{ticker.upper()} finns inte i databasen', color=0xDC143C)
    if not e:
        e = embed_message('KSE Bot', 'Error', f'Fel syntax. .c (kortnamn) (board/-)', color=0xDC143C)
    await ctx.send(embed=e)


@bot.command()
async def stocks(ctx, player=None, ticker=None, quantity=0):
    if player is not None:
        try:
            player = get_from_user(ctx.guild.get_member(int(player.strip('<@!>'))).id)
        except Exception as e:
            print(e)
            if uuid_in_database(mc_name_to_UUID(player)):
                player = get_from_user_uuid(mc_name_to_UUID(player))

    def stocks_message(u):

        embed_stock = Embed(title=f'{UUID_to_mc_name(u[6])}s aktier', color=0x00d9ff)
        embed_stock.set_author(name="KSE Bot")
        embed_stock.set_thumbnail(url=mc_head(u[6]))

        total = 0
        print(get_user_stock(u[0]))
        for s in get_user_stock(u[0]):
            if s[0]:
                total += s[0] * get_price(s[1])[-1][0]
                price = prefix(get_price(s[1])[-1][0] * s[0])
                embed_stock.add_field(name=s[1], value=f"{s[0]} st\n{price[0]} {price[1]}mm", inline=False)
            print(get_price(s[1])[-1][0])

        total = prefix(total)
        embed_stock.add_field(name="TOTAL", value=f"{total[0]} {total[1]}mm")

        return embed_stock

    e = ''
    if await command_in_command_channel(ctx):
        if player is None:
            u = get_from_user(ctx.author.id)
            e = stocks_message(u)
        elif ticker is None:
            if uuid_in_database(player[6]):
                u = player
                e = stocks_message(u)
            else:
                e = embed_message('KSE Bot', 'Error', f'Spelare är inte i databas', color=0xDC143C)
        elif ticker is not None:
            r = user_stock_uuid(player[6], ticker, quantity, ctx.author.id)
            if r[0]:
                e = embed_message('KSE Bot', 'Aktieinnehav', r[1], color=0x7FFF00)
            else:
                e = embed_message('KSE Bot', 'Aktieinnehav', r[1], color=0xDC143C)
        else:
            pass

    await ctx.send(embed=e)


@bot.command()
async def test(ctx):
    await utils.get(ctx.guild.channels, id=905425195064512563).send("hej")
    pass


@bot.command()
async def admin(ctx):
    if staff_perm(ctx.author.id):
        await update_names(ctx)


async def update_names(ctx):
    for i in ctx.channel.members:
        try:
            nick = UUID_to_mc_name(get_from_user(i.id)[6])
            await i.edit(nick=nick)
        except Exception as e:
            print(i, e)

bot.run(TOKEN)