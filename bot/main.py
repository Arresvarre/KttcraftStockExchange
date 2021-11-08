import os

from discord import *
from discord.ext import commands

intents = Intents.default()
intents.members = True
intents.messages = True

#command_channel_ids = (822020156065579032, 905425177557483562)
TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

bot = commands.Bot(command_prefix=".", intents=intents)

from dbfunc import *
from mc import *
from ksedb import *



#def log_channel():
#    id = os.getenv("LOG_ID")
#    return bot.get_channel(int(id))
#
#
#def embed_message(author, cause, text, thumbnail=None, color=0x00d9ff, footer=None):
#    embed = Embed(title=cause, description=text, color=color)
#    embed.set_author(name=author)
#    if thumbnail:
#        embed.set_thumbnail(url=thumbnail)
#    if footer:
#        embed.set_footer(text=footer)
#    return embed
#
#
#async def command_in_command_channel(ctx):
#    if ctx.channel.id == 822020156065579032 or ctx.channel.id == 905425177557483562:
#        return True
#    else:
#        await ctx.message.delete()
#        return False
#
#
#@bot.event
#async def on_ready():
#    await log_channel().send(embed=embed_message('KSE LOG', 'Ansluten', '', color=0x7FFF00))
#
#
#@bot.event
#async def on_member_join(m):
#    await log_channel().send(embed=embed_message('KSE LOG', f'{m.name} har gått med',f'ID:{m.id}',thumbnail=str(m.avatar_url)))
#
#
#@bot.event
#async def on_member_remove(m):
#    await log_channel().send(embed=embed_message('KSE LOG', f'{m.name} har lämnat',f'ID:{m.id}',thumbnail=str(m.avatar_url)))
#
#
#@bot.event
#async def on_message_edit(m, m2):
#    if not m.author == bot.user:
#        await log_channel().send(embed=embed_message('KSE LOG', f'{m.author.name} har ändrat ett meddelande',f'Innan:\n {m.content}\nEfter:\n {m2.content}', thumbnail=m.author.avatar_url, footer=f'MessageID: {m.id}'))
#
#
#@bot.command()
#async def user(ctx, user:Member = None, mc_name = None):
#    e = ''
#    if await command_in_command_channel(ctx):
#        if mc_name == None:
#            if user == None:
#                user = ctx.author
#            if user_in_database(user.id):
#                user = get_from_user(user.id)
#                e = embed_message('KSE Bot', UUID_to_mc_name(user[6]),
#                                  f'-INFO-\n'
#                                  f'UUID : {user[6]}\n'
#                                  f'DiscordId : {user[1]}\n'
#                                  f'Behörighet : {bool(user[5])} {bool(user[4])}\n '
#                                  f'Tillagd : {user[2]} av {UUID_to_mc_name(get_from_user_id(user[3])[6])}',
#                                  thumbnail=mc.mc_head(user[6]))
#            else:
#                raise commands.MemberNotFound('Not found player')
#        else:
#            if valid_mc_name(mc_name):
#                uuid = mc_name_to_UUID(mc_name)
#                a = add_user(user.id, uuid, ctx.author.id)
#                if a[0]:
#                    e = embed_message('KSE Bot', 'Lade till seplare i databas', a[1], color=0x7FFF00, thumbnail=mc.mc_head(uuid))
#                else:
#                    e = embed_message('KSE Bot', 'Error', a[1], color=0xDC143C)
#            else:
#                e = embed_message('KSE Bot', 'Error', 'Minecraft namnet måste finnas...' ,color=0xDC143C)
#        await ctx.send(embed=e)
#
#
#
#@user.error
#async def user_error(ctx, error):
#    e = ''
#    if await command_in_command_channel(ctx):
#        print(error)
#        if isinstance(error, commands.MemberNotFound):
#            e = embed_message('KSE Bot', 'Error', 'Hittade inte spelare. Måste anges med ett @', color=0xDC143C)
#        elif isinstance(error, commands.errors.CommandInvokeError) or isinstance(error, commands.MissingRequiredArgument):
#            e = embed_message('KSE Bot', 'Error', '.user user mc_name \n Exempel: \n .user @Arivd ZVAR3N', color=0xDC143C)
#        await ctx.send(embed=e)
#
#
#
#
#
@bot.command()
async def test(ctx):
    await ctx.send(ksedb.get_from_user(ctx.author.id))
    pass

bot.run(TOKEN)