import os, asyncio
from google_images_download import google_images_download


import discord
from discord.ext import commands


class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.searches = {}

    @commands.command(aliases=['img'])
    async def image(self, ctx, *, search:str):

        response = google_images_download.googleimagesdownload()
        arguments = {"keywords":search, "no_download":True}
        print(arguments)
        image_urls = response.download(arguments)

        if ctx.guild.id in self.searches:
            if self.searches[ctx.guild.id] is not None:
                l = self.searches[ctx.guild.id]
                l.update(image_urls[0])
                self.searches[ctx.guild.id] = l
        else:
            self.searches[ctx.guild.id] = []
            self.searches[ctx.guild.id] = image_urls[0]

        maxPage = int(len(self.searches[ctx.guild.id][search]))

        firstRun = True
        while True:
            if firstRun:
                firstRun = False
                num = 1

                url=self.searches[ctx.guild.id][search][0]
                msg = await ctx.channel.send(url)

            if maxPage == 1 and num == 1:
                print('{}/{}'.format(str(num),str(maxPage)))
                toReact = ['✅']
            elif num == 1:
                print('{}/{}'.format(str(num),str(maxPage)))
                toReact = ['⏩', '✅']
            elif num == maxPage:
                print('{}/{}'.format(str(num),str(maxPage)))
                toReact = ['⏪', '✅']
            elif num > 1 and num < maxPage:
                print('{}/{}'.format(str(num),str(maxPage)))
                toReact = ['⏪', '⏩', '✅']

            for reaction in toReact:
                await msg.add_reaction(reaction)
            
            def checkReaction(reaction, user):
                e = str(reaction.emoji)
                return e.startswith(('⏪', '⏩', '✅')) and reaction.message.id == msg.id and user.id != msg.author.id
            try:
                res = await self.bot.wait_for('reaction_add', timeout=60, check=checkReaction)
                if res is None:
                    await self.bot.delete_message(ctx.message)
                    await self.bot.delete_message(msg)
                    break
                elif res[0].emoji == '⏪':
                    num = num - 1

                    url=self.searches[ctx.guild.id][search][num-1]
                    await msg.delete()
                    msg = await ctx.channel.send(url)
                elif res[0].emoji == '⏩':
                    num = num + 1
                    
                    url=self.searches[ctx.guild.id][search][num-1]
                    await msg.delete()
                    msg = await ctx.channel.send(url)
                elif res[0].emoji == '✅':
                    await msg.clear_reactions()
                    break
            except:
                await msg.clear_reactions()
                break

def setup(bot):
    bot.add_cog(Google(bot))
