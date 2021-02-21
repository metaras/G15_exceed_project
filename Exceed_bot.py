import discord
import os
import json
import random
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
from discord import team, message
from discord.client import Client
from discord.ext import commands
#from dotenv import load_dotenv

mongo_url = "mongodb://exceed_group15:qt63ba2n@158.108.182.0:2255/exceed_group15"

cluster = MongoClient('mongodb://exceed_group15:qt63ba2n@158.108.182.0:2255/exceed_group15')
db = cluster["exceed_group15"]
collection_A = db['mall_A']
collection_B = db['mall_B']
collection_A_y = db['mall_A_yesterday']
collection_B_y = db['mall_B_yesterday']
time_A = db['time_A']
time_B = db['time_B']
time_A_y = db['time_A_yesterday']
time_B_y = db['time_B_yesterday']
time_A_a = db['time_A_average']
time_B_a = db['time_B_average']

client = discord.Client()
@client.event
async def on_ready():
    print(f"connected")


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if message.content == '!help':

        embed1 = discord.Embed(title = "ท่านผู้เจริญ Command:",color = discord.Colour.gold())
        #embed.set_image(url = 'https://tenor.com/view/keqing-genshin-impact-genshin-impact-god-gif-19879828')
        #embed.set_thumbnail(url='https://upload-os-bbs.mihoyo.com/upload/2020/01/23/1015158/c870945193b1b3eebe2cb1beb53ccba1_3336201567560481242.gif')
        #embed.add_field(name='',value ='--->',inline=False)
        embed = discord.Embed(title = "[Present Command]",color = discord.Colour.green())
        embed.add_field(name='"status bar"',value = "Description: return the current bar graph of people inside mall A and mall B by time",inline=True)
        embed.add_field(name='"status in&out A bar"',value = "Description: return bar graph of comparison of people coming in&out of mall A",inline=True)
        embed.add_field(name='"status in&out B bar"',value = "Description: return bar graph of comparison of people coming in&out of mall B",inline=True)
        embed.add_field(name='"status line"',value = "Description: return the current line graph of people inside mall A and mall B by time",inline=True)
        embed.add_field(name='"status in&out A line"',value = "Description: return line graph of comparison of people coming in&out of mall A",inline=True)
        embed.add_field(name='"status in&out B line"',value = "Description: return line graph of comparison of people coming in&out of mall B",inline=True)
        embed.add_field(name='"status (A/B)"',value = "Description: return the current status of people inside the mall A or mall B",inline=True)
        embed.add_field(name='"status pie (A/B)"',value = "Description: return the current pie graph of people which are accepted and rejected in mall A or mall B",inline=True)
        embed.add_field(name='"status compare"',value = "Description: return pie graph of comparison of people inside mall A and mall B",inline=True)
        embed.add_field(name='"status compare visited"',value = "Description: return pie graph of comparison of people visited mall A and mall B",inline=True)
        
        #embed.add_field(name='',value ='--->')
        embed2 = discord.Embed(title = "[Previous Command]",color = discord.Colour.red())
        embed2.add_field(name='"prev bar"',value = "Description: return yesterday bar graph of people inside mall A and mall B by time",inline=True)
        embed2.add_field(name='"prev in&out A bar"',value = "Description: return yesterday bar graph of comparison of people coming in&out of mall A",inline=True)
        embed2.add_field(name='"prev in&out B bar"',value = "Description: return yesterday bar graph of comparison of people coming in&out of mall B",inline=True)
        embed2.add_field(name='"prev line"',value = "Description: return yesterday line graph of people inside mall A and mall B by time",inline=True)
        embed2.add_field(name='"prev in&out A line"',value = "Description: return yesterday line graph of comparison of people coming in&out of mall A",inline=True)
        embed2.add_field(name='"prev in&out B line"',value = "Description: return yesterday line graph of comparison of people coming in&out of mall B",inline=True)
        embed2.add_field(name='"prev (A/B)"',value = "Description: return yesterday status of people inside the mall A or mall B",inline=True)
        embed2.add_field(name='"prev pie (A/B)"',value = "Description: return yesterday pie graph of people which are accepted and rejected in mall A or mall B",inline=True)
        embed2.add_field(name='"prev compare visited"',value = "Description: return yesterday pie graph of comparison of people visited mall A and mall B",inline=True)

        #embed.add_field(name='status',value = "Description: return the current status of people inside the mall\n Usage:   status (A/B)",inline=False)
        embed3 = discord.Embed(title = "[Prediction Command]",color = discord.Colour.blue())
        embed3.add_field(name='"predict bar"',value = "Description: return prediction bar graph of people inside mall A and mall B by time",inline=True)
        #embed3.add_field(name='"predict in&out A bar"',value = "Description: return prediction bar graph of comparison of people coming in&out of mall A",inline=True)
        #embed3.add_field(name='"predict in&out B bar"',value = "Description: return prediction bar graph of comparison of people coming in&out of mall B",inline=True)
        embed3.add_field(name='"predict line"',value = "Description: return prediction line graph of people inside mall A and mall B by time",inline=True)
        #embed3.add_field(name='"predict in&out A line"',value = "Description: return prediction line graph of comparison of people coming in&out of mall A",inline=True)
        #embed3.add_field(name='"predict in&out B line"',value = "Description: return prediction line graph of comparison of people coming in&out of mall B",inline=True)
        await message.channel.send('จ้ะเอ๋ ตัวเอง')
        await message.channel.send(embed = embed1)
        await message.channel.send(embed = embed)
        await message.channel.send(embed = embed2)
        await message.channel.send(embed = embed3)
    

    
    elif message.content == 'status A':
        peopledense = {"name": "people&density"}
        people_in = {"name": "cumming_in"}
        people_out = {"name": "cumming_out"}
        people_temp = {"name": "temp"}

        peopledense_branch = collection_A.find_one(peopledense)
        people_in_branch = collection_A.find_one(people_in)
        people_out_branch = collection_A.find_one(people_out)
        people_temp_branch = collection_A.find_one(people_temp)

        people = peopledense_branch['people']
        density = peopledense_branch['density']
        p_in = people_in_branch['in']
        p_out = people_out_branch['out']
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 

        embed = discord.Embed(title = "Current status in mall A",color = discord.Colour.red())
        embed.add_field(name='Number of people inside:',value = people ,inline=True)
        embed.add_field(name='People visited:',value = p_in ,inline=True)
        embed.add_field(name='People accepted:',value = p_pass ,inline=True)
        embed.add_field(name='Density of people inside:',value = density,inline=True)
        embed.add_field(name='People Leaved:',value = p_out,inline=True)
        embed.add_field(name='People rejected:',value = p_npass,inline=True)

        await message.channel.send(embed=embed)
    
    elif message.content == 'status B':
        peopledense = {"name": "people&density"}
        people_in = {"name": "cumming_in"}
        people_out = {"name": "cumming_out"}
        people_temp = {"name": "temp"}

        peopledense_branch = collection_B.find_one(peopledense)
        people_in_branch = collection_B.find_one(people_in)
        people_out_branch = collection_B.find_one(people_out)
        people_temp_branch = collection_B.find_one(people_temp)

        people = peopledense_branch['people']
        density = peopledense_branch['density']
        p_in = people_in_branch['in']
        p_out = people_out_branch['out']
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 

        embed = discord.Embed(title = "Current status in mall B",color = discord.Colour.red())
        embed.add_field(name='Number of people inside:',value = people ,inline=True)
        embed.add_field(name='People visited:',value = p_in ,inline=True)
        embed.add_field(name='People accepted:',value = p_pass ,inline=True)
        embed.add_field(name='Density of people inside:',value = density,inline=True)
        embed.add_field(name='People Leaved:',value = p_out,inline=True)
        embed.add_field(name='People rejected:',value = p_npass,inline=True)

        await message.channel.send(embed=embed)

    elif message.content == 'status line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People inside the malls by time', ylabel='mall A')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='mall B')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status in&out A line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status in&out B line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='Mall_A')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='Mall_B')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People inside the malls by time')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
        
    elif message.content == 'status in&out A bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall A by time')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status in&out B bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall B by time')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status pie A':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch = collection_A.find_one({"name": "temp"})
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'accepted'
        p_npass = str(p_npass)+' '+'rejected'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="Scanned people",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Scanner: Mall A")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
    
    elif message.content == 'status pie B':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch = collection_B.find_one({"name": "temp"})
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'accepted'
        p_npass = str(p_npass)+' '+'rejected'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="Scanned people",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Scanner: Mall B")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status compare':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch_A = collection_A.find_one({"name": "people&density"})
        people_temp_branch_B = collection_B.find_one({"name": "people&density"})
        p_pass = people_temp_branch_A['people']
        p_npass = people_temp_branch_B['people'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'mall_A'
        p_npass = str(p_npass)+' '+'mall_B'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="People inside: ",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Comparison of people inside mall A&B")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'status compare visited':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch_A = collection_A.find_one({"name": "cumming_in"})
        people_temp_branch_B = collection_B.find_one({"name": "cumming_in"})
        p_pass = people_temp_branch_A['in']
        p_npass = people_temp_branch_B['in'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'mall_A'
        p_npass = str(p_npass)+' '+'mall_B'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="People visited: ",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Comparison of people visited mall A&B")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)










    elif message.content == 'prev A':
        peopledense = {"name": "people&density"}
        people_in = {"name": "cumming_in"}
        people_out = {"name": "cumming_out"}
        people_temp = {"name": "temp"}

        peopledense_branch = collection_A_y.find_one(peopledense)
        people_in_branch = collection_A_y.find_one(people_in)
        people_out_branch = collection_A_y.find_one(people_out)
        people_temp_branch = collection_A_y.find_one(people_temp)

        people = peopledense_branch['people']
        density = peopledense_branch['density']
        p_in = people_in_branch['in']
        p_out = people_out_branch['out']
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 

        embed = discord.Embed(title = "Yesterday status in mall A",color = discord.Colour.red())
        embed.add_field(name='Number of people inside:',value = people ,inline=True)
        embed.add_field(name='People visited:',value = p_in ,inline=True)
        embed.add_field(name='People accepted:',value = p_pass ,inline=True)
        embed.add_field(name='Density of people inside:',value = density,inline=True)
        embed.add_field(name='People Leaved:',value = p_out,inline=True)
        embed.add_field(name='People rejected:',value = p_npass,inline=True)

        await message.channel.send(embed=embed)
    
    elif message.content == 'prev B':
        peopledense = {"name": "people&density"}
        people_in = {"name": "cumming_in"}
        people_out = {"name": "cumming_out"}
        people_temp = {"name": "temp"}

        peopledense_branch = collection_B_y.find_one(peopledense)
        people_in_branch = collection_B_y.find_one(people_in)
        people_out_branch = collection_B_y.find_one(people_out)
        people_temp_branch = collection_B_y.find_one(people_temp)

        people = peopledense_branch['people']
        density = peopledense_branch['density']
        p_in = people_in_branch['in']
        p_out = people_out_branch['out']
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 

        embed = discord.Embed(title = "Yesterday status in mall B",color = discord.Colour.red())
        embed.add_field(name='Number of people inside:',value = people ,inline=True)
        embed.add_field(name='People visited:',value = p_in ,inline=True)
        embed.add_field(name='People accepted:',value = p_pass ,inline=True)
        embed.add_field(name='Density of people inside:',value = density,inline=True)
        embed.add_field(name='People Leaved:',value = p_out,inline=True)
        embed.add_field(name='People rejected:',value = p_npass,inline=True)

        await message.channel.send(embed=embed)

    elif message.content == 'prev line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B_y.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People inside the malls by time (Yesterday)', ylabel='mall A')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='mall B')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'prev in&out A line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'prev in&out B line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'prev bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B_y.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='Mall_A')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='Mall_B')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People inside the malls by time (yesterday)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
    
    elif message.content == 'prev in&out A bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall A by time (Yesterday)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'prev in&out B bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B_y.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall B by time (Yesterday)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
        

    elif message.content == 'prev pie A':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch = collection_A_y.find_one({"name": "temp"})
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'accepted'
        p_npass = str(p_npass)+' '+'rejected'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="Scanned people",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Scanner(Yesterday): Mall A")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
    
    elif message.content == 'prev pie B':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch = collection_B_y.find_one({"name": "temp"})
        p_pass = people_temp_branch['pass']
        p_npass = people_temp_branch['not_pass'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'accepted'
        p_npass = str(p_npass)+' '+'rejected'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="Scanned people",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Scanner(Yesterday): Mall B")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
    
    elif message.content == 'prev compare visited':
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        people_temp_branch_A = collection_A_y.find_one({"name": "cumming_in"})
        people_temp_branch_B = collection_B_y.find_one({"name": "cumming_in"})
        p_pass = people_temp_branch_A['in']
        p_npass = people_temp_branch_B['in'] 
        pie_info =[p_pass,p_npass]
        explode = (0, 0.1)
        p_pass = str(p_pass)+' '+'mall_A'
        p_npass = str(p_npass)+' '+'mall_B'
        # print(p_pass)
        # print(p_npass)
        recipe = [p_pass,p_npass]

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        

        def func(pct, allvals):
            # print(pct)
            absolute = int(pct/100.*np.sum(allvals))
            a= "{:.0f}%\n({:d} people)".format(pct, absolute)
            # print(pct)
            # print(a)
            return a

        # print(data)
        # print(pct)
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        #print(wedges[1])
        ax.legend(wedges, ingredients,
                title="People visited yesterday: ",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Comparison of people visited mall A&B (Yesterday)")
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)












    elif message.content == 'predict line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B_a.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People inside the malls by time (Prediction)', ylabel='mall A')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='mall B')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'predict in&out A line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'predict in&out B line':
        labels_1 = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        labels_2 = labels_1
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10
        #print(set_time_A)
        #print(set_time_B)
        fig, (ax1, ax2) = plt.subplots(2, sharey=True)
        ax1.plot(labels_1, set_time_A, 'ko-')
        ax1.set(title='People coming in&out mall A by time', ylabel='IN')

        ax2.plot(labels_2, set_time_B, 'r.-')
        ax2.set(xlabel='time', ylabel='OUT')

        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'predict bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                set_time_A.append(time_branch_A['people'])
            start_time = int(start_time)+1
        start_time = 10
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_B = time_B_a.find_one({'start':start_time})
            if time_branch_B ==None:
                set_time_B.append(0)
            else:
                set_time_B.append(time_branch_B['people'])
            start_time = int(start_time)+1

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='Mall_A')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='Mall_B')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People inside the malls by time (Prediction)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'predict in&out A bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_A_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall A by time (Prediction)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)

    elif message.content == 'predict in&out B bar':
        
        labels = ['11am', '12am', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm','10pm']
        start_time = 10
        set_time_A =[]
        set_time_B =[]
        while start_time <= 21:
            start_time = str(start_time)
            time_branch_A = time_B_a.find_one({'start':start_time})
            if time_branch_A ==None:
                set_time_A.append(0)
            #print(time_branch_A)
            else:
                #print(time_branch_A)
                set_time_A.append(time_branch_A["in"])
                set_time_B.append(time_branch_A["out"])
            start_time = int(start_time)+1
        start_time = 10

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, set_time_A, width, label='IN')
        rects2 = ax.bar(x + width/2, set_time_B, width, label='OUT')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('number of people')
        ax.set_title('People coming in&out mall B by time (Prediction)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()


        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        #plt.show()
        plt.savefig("test.png")
        image = discord.File("test.png")
        plt.close()
        await message.channel.send(file=image)
        

    
    # elif message.content == 'pie':
    #     await message.channel.send('compiling')
    #     people_temp = {"name": "temp"}
    #     people_temp_branch = collection_A.find_one(people_temp)
    #     p_pass = people_temp_branch['pass']
    #     p_npass = people_temp_branch['not_pass'] 
    #     pie_info =[p_pass,p_npass]
    #     explode = (0, 0.1)
    #     labels = 'normal temperature','high temperature(rejected)'
    #     plt.pie(pie_info, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    #     plt.savefig("test.png")
    #     image = discord.File("test.png")
    #     plt.close()
    #     await message.channel.send(file=image)
    # elif message.content == 'graph':
    #     await message.channel.send('compiling')
    #     x = [1,2,3,4]
    #     y = [1,2,3,4]
    #     plt.plot(x,y)
    #     plt.savefig("test.png")
    #     image = discord.File("test.png")
    #     plt.close()
    #     await message.channel.send(file=image)

    # elif message.content == 'rgraph':
    #     await message.channel.send('compiling')
    #     start_time = 10
    #     set_time =[]
    #     while start_time <= 21:
    #         start_time = str(start_time)
    #         time_branch = time_A.find_one({'start':start_time})
    #         set_time.append(time_branch['people'])
    #         start_time = int(start_time)+1
    #     labels = ['10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22']
    #     print(set_time)
    #     plt.bar(labels, set_time)
    #     plt.savefig("test.png")
    #     image = discord.File("test.png")
    #     plt.close()
    #     await message.channel.send(file=image)
    # elif message.content == 'current density A':
    #     today = {"name": "people&density"}
    #     x = collection_A.find_one(today)
    #     density = x['density']
    #     response = f"The current density is {density} people per m^2."
    #     await message.channel.send(response)
    # elif message.content == 'current people A':
    #     today = {"name": "people&density"}
    #     x = collection_A.find_one(today)
    #     people = x['people']
    #     response = f"Currently, there are {people} people inside."
    #     await message.channel.send(response)
    elif message.content.startswith('ice'):
        await message.channel.send('compiling')
    if message.content.startswith('dukdik1'):
        await message.channel.send('https://i.gifer.com/7OWi.gif')
    if message.content.startswith('dukdik2'):
        await message.channel.send('https://i.pinimg.com/originals/1f/89/62/1f89628ff36c6b1ecebe8a01f0d439cb.gif')
    # elif message.content.startswith('get'):
    #     date = msg[4:]
    #     response = f"searching graph in {date}"
    #     await message.channel.send(response)
    #     graph = collection.find(date)
    #     await message.channel.send(graph[0])    
    # elif message.content.startswith('insert'):
    #     #await message.channel.send('1')
    #     #filt = {'_id':'602ccb7df9311b0008f263be'}
    #     #x = collection.find_one(filt)
    #     #collection.update_one({$set:{'count':x['count']+1}})
    #     ins =msg[7:]
    #     insert_num = {'inserted_num':ins}
    #     collection.insert_one(insert_num)
    #     response = f"inserted {ins}"
    #     await message.channel.send(response)

#collection.insert_one({'1':'this is your 1/1/1 graph'})
#collection.insert_one({'2':'this is your 1/1/2 graph'})
#collection.insert_one({'3':'this is your 1/1/3 graph'})
#collection.insert_one({'4':'this is your 1/1/4 graph'})
#collection.insert_one({'5':'this is your 1/1/5 graph'})
#x = collection.find()
#print(x[1]['1/2/3'])
#collection.insert_one({'insert_test':'hi'})
client.run('')