from twitchio.ext import commands
import json
import os
import time

class Bot(commands.Bot):
    OAUTH = os.environ['TWITCH_OAUTH']
    ID = os.getenv('TWITCH_ID')
    print(OAUTH, ID)

    def __init__(self):
        super().__init__(irc_token=self.OAUTH, client_id=self.ID, nick='boxingb0t', prefix='-',
                         initial_channels=['Toxic_HoneyBadger'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')


    async def event_message(self, message):
        print(f'<{message.author.name}> {message.content}\n')
        await self.handle_commands(message)

        with open('points.json', 'r') as f:
            users = json.load(f)

        await self.add_user(message.author, users)

        with open('points.json', 'w') as f:
            users = json.dump(users, f)

    # Commands use a decorator...
    @commands.command(name='box')
    async def box(self, ctx, challenger, wager):
        wager = int(wager)
        if wager >= 10:
            await ctx.send_me(f'{ctx.author.name} has challenged {challenger} for {wager} coins!')
            time.sleep(2)
            await ctx.send_me( f'{challenger} please type -accept to box {ctx.author.name} for {wager} coins!')
        else:
            await ctx.send(f'{ctx.author.id} you must challenge a person for 10 coins or more')
    @box.error
    async def bot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Syntax Error: -box {challeneger} {wager amount}')

    @commands.command(name='accept')
    async def accept(self, ctx):
        if box.challenger == ctx.author.name:
            await ctx.send_me(f'{ctx.author.id} has challenged {challenger} for {wager} coins!', f'{challenger} please type -accept to box {ctx.author.name} for {wager} coins!')

    @commands.command(name='points')
    async def points(self, ctx):
        with open('points.json', 'r') as f:
            users = json.load(f)
        points = users[f"{ctx.author.id}"]["points"]
        print(points)
        await ctx.send(f'{ctx.author.name} have {points} points')
    
    async def add_user(self, author, users):
        if not f"{author.id}" in users:
            users[author.id] = {}
            users[author.id]['points'] = 100
            
bot = Bot()
bot.run()