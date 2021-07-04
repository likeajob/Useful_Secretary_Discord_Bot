import discord
import os
import sqlite3
import os.path
import datetime

from discord.message import Message

client = discord.Client()

# connect to database
if os.path.isfile('money_saver.db'):
    con = sqlite3.connect('money_saver.db')
    cur = con.cursor()
else:
    con = sqlite3.connect('money_saver.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE user_info
               (user_id text not null primary key,
               user_name text not null,
               total_worth real)''')

    cur.execute('''CREATE TABLE transactions
               (id INTEGER not null primary key,
               user_id text references user_info,
               amount real,
               time timestamp)''')

    # cur.execute('''INSERT INTO user_info
    #            VALUES ('240359026746064917','lkj#6434', 2000.00)''')

    # con.commit()


async def get_all_user():
    users = cur.execute("SELECT * from user_info")
    return users


async def add_user(id, name, total=0):
    cur.execute(f"INSERT INTO user_info VALUES ('{id}', '{name}', {total})")
    con.commit()
    user = cur.execute(
        "SELECT user_name from user_info where user_id = {0}".format(id))
    return user


async def create_tx(user, amount):
    time = datetime.datetime.now()
    print(time)
    cur.execute(
        f"INSERT INTO transactions (user_id, amount, time) VALUES ('{user.id}', {amount}, '{time}')")
    con.commit()
    return cur.lastrowid


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    authur = message.author
    content = message.content
    if message.author == client.user:
        return

    if content.startswith('$test'):
        await message.channel.send("Hello you little sh*t")
        
    if content.startswith('เบียร์'):
        await message.channel.send("เหลี่ยมไม่ไหว")

    if content.startswith(('$new', '$n')):
        users = await get_all_user()
        ids = []
        for row in users:
            ids.append(row[0])

        contents = content.split(' ')
        if len(contents) == 2:
            amount = str(contents[1])
            print(amount.isnumeric())
            if amount.isnumeric():
                amount = float(amount)
                if (str(authur.id) not in ids):
                    await add_user(str(authur.id), str(authur))
                    await message.channel.send(f"{authur} add to database")
                id = await create_tx(authur, amount)
                await message.channel.send(f"#{id} Transaction added")
            else:
                await message.channel.send("amount should be numeric")
        else:
            await message.channel.send("command should be \"$new amount\"")

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
