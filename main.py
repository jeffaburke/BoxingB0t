from twitchio.ext import commands
import json
from impVar import OAUTH, ID

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=OAUTH, client_id=ID, nick='boxingb0t', prefix='-',
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
        if wager > 9:
            await ctx.send_me(f'{ctx.author.name} has challenged {challenger} for {wager} coins!')
            await ctx.send_me(f'{challenger} please type -accept to box {ctx.author.name} for {wager} coins!')
        else:
            await ctx.send(f'{ctx.author.name} you must challenge a person for 10 coins or more')
    @box.error
    async def bot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Syntax Error: -box {challeneger} {wager amount}')

    @commands.command(name='accept')
    async def accept(self, ctx):
        if box.challenger == ctx.author.name:
            await ctx.send_me(f'{ctx.author.name} has challenged {challenger} for {wager} coins!')
            await ctx.send_me(f'{challenger} please type -accept to box {ctx.author.name} for {wager} coins!')

    async def add_user(slf, author, users):
        if not author.id in users:
            users[author.id] = {}
            users[author.id]['points'] = 100
            
bot = Bot()
bot.run()