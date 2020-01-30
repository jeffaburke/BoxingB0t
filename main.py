from twitchio.ext import commands
import json
import os
import time
import random

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
        with open('points.json', 'r') as f:
            users = json.load(f)
        self.challenger = challenger
        self.boxer = ctx.author
        wager = int(wager)
        self.wager = wager
        if wager >= 10:
            if users[f"{ctx.author.id}"]["points"] >= wager:
                await ctx.send_me(f'{ctx.author.name} has challenged {challenger} for {wager} coins!')
                time.sleep(2)
                await ctx.send_me(f'{challenger} please type -accept to box {ctx.author.name} for {wager} coins!')
            else:
                ctx.send_me(f"{ctx.author.name} you need more points, do -points to see how many you have!")
        else:
            await ctx.send(f'{ctx.author.name} you must challenge a person for 10 coins or more')
        with open('points.json', 'w') as f:
            users = json.dump(users, f)
    @box.error
    async def bot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Syntax Error: -box {challenger} {wager amount}')

    @commands.command(name='accept')
    async def accept(self, ctx):
        match = random.randint(1, 2)
        challenger = self.challenger
        boxer = self.boxer
        challenger = challenger.lower()
        wager = self.wager
        with open('points.json', 'r') as f:
            users = json.load(f)
        if challenger == ctx.author.name:
            if users[f"{ctx.author.id}"]["points"] >= wager:
                with open('points.json', 'r') as f:
                    users = json.load(f)
                if match == 1:
                    await ctx.send_me(f'{ctx.author.name} has lost against {boxer.name} and lost {wager} coins!')
                    print(f"{boxer.id} won {wager}")
                    users[f"{boxer.id}"]["points"] += wager
                    users[f"{ctx.author.id}"]["points"] -= wager
                else:
                    await ctx.send_me(f'{ctx.author.name} has won against {boxer.name} and gained {wager} coins!')
                    print(f"{ctx.author.id} won {wager}")
                    users[f"{ctx.author.id}"]["points"] += wager
                    users[f"{boxer.id}"]["points"] -= wager
                with open('points.json', 'w') as f:
                    users = json.dump(users, f)
            else:
                await ctx.send(f'{ctx.author.name} you must challenge a person for 10 coins or more')
        else:
            print("FAIL ON USER ACCEPT")

        

    @commands.command(name='points')
    async def points(self, ctx):
        with open('points.json', 'r') as f:
            users = json.load(f)
        points = users[f"{ctx.author.id}"]["points"]
        await ctx.send(f'{ctx.author.name} has {points} points')
    
    async def add_user(self, author, users):
        if not f"{author.id}" in users:
            users[author.id] = {}
            users[author.id]['points'] = 100
            
bot = Bot()
bot.run()