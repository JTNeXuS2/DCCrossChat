## -*- coding: utf-8 -*-
## -*- coding: cp1251 -*-
import disnake as discord
import os
import sys
import requests
import json
import re
import unicodedata
import urllib.parse
import aiohttp
import asyncio
import configparser
import hashlib

from disnake.ext import commands
from disnake import Intents

urlhook = "http://junger.zzux.com/webhook/prcon.php"
lookchanel = []
fname = 'secur/Clist.txt'
ftoken = 'secur/Token.txt'
flic = 'secur/lickey.txt'
seed = "PUBLICSEED"
# Остановить выполнение кода и вывести сообщение остановки
def stop_execution():
    print("Press Enter to Exit...")
    input() # Ожидание нажатия клавиши Enter
    sys.exit()

def cteatetemplatetoken(file_name):
  try:
      if not os.path.exists('secur'):
        os.mkdir('secur')
      with open(file_name, 'w') as file:
        file.write('\n')
  except Exception as e:
      print(f"Cant create config files: {str(e)}")

def create_config_ini():
    try:
        if not os.path.exists('secur'):
            os.mkdir('secur')
        config_data = ''';host = address
;port = rcon port
;pass = rcon pass
;chat=(1-PIPPI, 2-AmunatServerTransfer) - chat system message type on server, need installed mod

[exiles]
host=192.168.0.101
port=9780
pass=123456

[siptah]
host=junger.zzux.com
port=9780
pass=123456
chat=2
'''
        with open('./secur/config.ini', 'w') as config_file:
            config_file.write(config_data)
    except Exception as e:
        print(f"Cannot create config.ini file: {str(e)}")

def chektemplate():
    if not os.path.exists('secur'):
        os.mkdir('secur')
    if not os.path.exists(fname):
        print(' A file '+str(fname)+ ' List channels ID to tracked, Fill it or use /lookhere in discord channel (need admin rigts)')
        cteatetemplatetoken(fname)
    if not os.path.exists(ftoken):
        print(' A file '+str(ftoken)+ ' has been created. Write the token received from your application into it\n>> https://discord.com/developers/applications/\n')
        cteatetemplatetoken(ftoken)
    if not os.path.exists(flic):
        print(' A file '+str(flic)+ ' public key has been created. Write your key into it and restart the application\n')
        cteatetemplatetoken(flic)
    if not os.path.exists('./secur/config.ini'):
        print(' A file '+str('./secur/config.ini')+ 'Server Lists\n')
        create_config_ini()

# Функция для чтения файла и заполнения переменной lookchanel
def read_channels():
    try:
        with open(fname, 'r') as file:
            for line in file:
                channel_id = line.strip()
                lookchanel.append(channel_id)
            return lookchanel
    except FileNotFoundError:
        # Если файл не найден, создаем его
        with open(fname, 'w') as file:
            pass
# Функция для записи переменной lookchanel в файл
def update_channels(lookchanel):
    # Считываем содержимое файла
    existing_channels = read_channels()
    # Объединяем считанные данные со значениями из lookchanel и удаляем дубликаты
    all_channels = list(set(lookchanel + existing_channels))
    # Записываем обновленные данные в файл
    with open(fname, 'w') as file:
        for channel_id in all_channels:
            file.write(channel_id + '\n')

def write_channels(lookchanel):
    # Записываем обновленные данные в файл
    lookchanel = list(set(lookchanel))
    with open(fname, 'w') as file:
        for channel_id in lookchanel:
            file.write(channel_id + '\n')

# Функция обработки команды /lookhere
def handle_lookhere(channel_id):
    if channel_id not in lookchanel:
        lookchanel.append(channel_id)
        update_channels(lookchanel)

# Функция обработки команды /deletehere
def handle_deletehere(channel_id):
    if channel_id in lookchanel:
        lookchanel.remove(channel_id)
        write_channels(lookchanel)

#проверим список
chektemplate()
#список каналов прослушки

def read_ftoken():
  TOKEN = ''
  with open(ftoken, "r") as file:
    TOKEN = file.read()
  return TOKEN

TOKEN = read_ftoken()
if len(str(TOKEN)) == 0:
  print('ERROR read Token:>>>> ' + str(TOKEN) + ' <<<\nToken cant null or invalid, Write the token received from your application into it\n>> https://discord.com/developers/applications\n')
  stop_execution()

#================================= lic chek
def read_flic():
  public_key = ''
  with open(flic, "r") as file:
    public_key = file.read()
  return public_key
public_key = read_flic()
if len(str(public_key)) == 0:
  print(f"ERROR read public_key\nFill secur\\lickey.txt")
print (' public key: ' + str(public_key))

url = 'http://junger.zzux.com/webhook/lic.php'
params = {'public_key': public_key}
response = requests.get(url, params=params)

if response.status_code == 200:  # Убедитесь, что ответ сервера успешный (код 200)
    try:
        data = response.json()  # Преобразуем полученные данные в JSON-формат

        if 'VALIDATE' in data:
            result = data['VALIDATE']
            code = data['secret']
            hashed_seed = hashlib.sha256(seed.encode()).hexdigest()
            if result and (hashed_seed == code):
                print(' chat token: '+str(code))
                print(' licensed: VALID\n')
            elif not result:
                print(' public key: INVALID')
                stop_execution()
            elif hashed_seed != code:
                print(' chat token: INVALID\n maybe app update?')
                stop_execution()
            else:
                print('Unexpected result:', result)
                stop_execution()
        else:
            print('Invalid server response', response.status_code)
            stop_execution()
    except Exception as e:
        print('Error occurred while converting data to JSON format:', e)
        stop_execution()
else:
    print(' Error when accessing. Response code:', response.status_code)
    stop_execution()
#================================= END chek

lookchanel = read_channels()

async def read_servers():
  # Считываем конфигурационный файл
  config = configparser.ConfigParser()
  config.read("./secur/config.ini")
  # Получаем все секции и значения
  servers = config.sections()
  if not servers:
    print('Server list is Empty!\nFill in the list of servers config secur/config.ini')
  return servers


intents = discord.Intents.default()
intents = discord.Intents().all()
prefix= ''
words = ['!help']
client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)



def strip_rcon_log(response, server):
    if response.lower() not in ['ok', 'ok.']:
        print(str(server)+' '+response)
    return

async def send_rcon_command(host, port, rcon_password, command, server, raise_errors=False, num_retries=3, timeout=4.0):
    from valve.rcon import RCON, RCONMessageError, RCONAuthenticationError, RCONMessage
    import socket

    try:
        port = int(port)
    except ValueError:
        return None

    attempts = 0
    while attempts < num_retries:
        attempts += 1
        try:
            with RCON((host, port), rcon_password, timeout=timeout) as rcon:
                RCONMessage.ENCODING = "utf-8"
                response = rcon(command)
                return strip_rcon_log(response, server)

        except KeyError:
            raise RconError('Incorrect rcon password')

        except (socket.error, socket.timeout, RCONMessageError, RCONAuthenticationError) as e:
            response = str(e)
            if attempts >= num_retries:
                if raise_errors:
                    raise RconError(str(e))
                else:
                    return strip_rcon_log(response, server)

async def compile_send(rank, color, dname, dmessage):
  # Считываем конфигурационный файл
  config = configparser.ConfigParser()
  config.read("./secur/config.ini")
  # Получаем все секции и значения
  servers = config.sections()
  if not servers:
    print('Server list is Empty!\nFill in the list of servers config secur/config.ini')
  # Получаем конфигурацию для указанного сервера
  for server in servers:
      host = config[server]['host']
      port = config[server]['port']
      rcon_password = config[server]['pass']
      chat = config[server].get('chat', '')  # По умолчанию пустая строка, если переменная отсутствует
      match chat:
           case "2":
               command = 'ast chat "global" '+dname+':'+dmessage
           case _:
               command = 'globallink cmd=globalchat&data='+ rank + '|' + color + '|' + dname + '|' + dmessage
      print(f"Command: {command}")
      await send_rcon_command(host, port, rcon_password, command, server)

async def show_help(message):
    await message.channel.send('Support commands\n'
    '/lookhere    - added this channel to tracked\n'
    '/deletehere  - remove this channel from tracking\n'
    '/update      - update and show servers\n'
    )

@bot.command(pass_context=True, intents=intents) #разрешаем передавать агрументы
async def test(ctx, arg): #создаем асинхронную фунцию бота
    await ctx.send(arg) #отправляем обратно аргумент

@client.event
async def on_ready():
  #print(f"{client.user} Hello World!")
  print('')
  print('We have logged in as {0.user}'.format(client))					#вывод в консоль по готовности
  await getServersName()
  if lookchanel == []:
    print('>> Channel list is empty\nTo add a monitored channel, type /lookhere in discord channel\n')
  print('Invite bot link to discord (open in browser):\nhttps://discord.com/api/oauth2/authorize?client_id='+ str(client.user.id) +'&permissions=8&scope=bot\n')

async def getServersName():
    for guild in client.guilds:
        id = guild.name
        print('Connect to ' + str(id))

@client.event
async def on_message(message):
  if message.author == client.user:		#отсеим свои сообщения
    return;
  if not any(map(message.content.__contains__, words)) and message.author.bot:					#отсеим сообщения ботов без запроса хелпа
    return;
  if message.author.bot:																		#отсеим сообщения ботов
    return;

  if str(message.channel.id) not in lookchanel:													# смотрим только каналы из списка!
      if message.content.startswith('/lookhere'):
          if message.author.guild_permissions.administrator:
              handle_lookhere(str(message.channel.id))
              print('Channel is tracked >>> ' + str(message.channel.id))
              await message.channel.send('Channel is tracked ' + str(message.channel.id))
          else:
              await message.channel.send('You do not have administrator rights')
      elif message.content.startswith('/chathelp'):
            await show_help(message)
            return
      return
  if message.author.guild_permissions.administrator:
      commands = message.content.split()
      if len(commands) > 0:
          command = commands[0]
          match command:
              case '/deletehere':
                  handle_deletehere(str(message.channel.id))
                  print('Channel is no longer tracked >>> ' + str(message.channel.id))
                  await message.channel.send('Channel is no longer tracked ' + str(message.channel.id))
                  return
              case '/update':
                  servers = await read_servers()
                  await message.channel.send('Server List\n' + str(servers) + '\nUpdated!')
                  return
              case '/chathelp':
                  await show_help(message)
                  return
  if message.content.startswith(''):															#если сообщение пришло, в '' можно сунуть прификс без которого игнор всех сообщений
    if message.content.startswith('/lookhere'):
      print('Channel is already being tracked >>> ' + str(message.channel.id))
      await message.channel.send('Channel is already being tracked ' + str(message.channel.id))

    # Инициализация message и заменяем ид на имена
    quote = message.content
    
    # Замена ид автора на имя
    dname = message.author.display_name or message.author.global_name or message.author.name
    # Замена упоминаний пользователей: <@user_id> или <@!user_id> на имя пользователя
    for user in message.mentions:
        name_to_use = user.display_name or user.global_name or user.name
        quote = re.sub(rf'<@!?{user.id}>', f'@{name_to_use}', quote)
    # Замена упоминаний ролей: <@&role_id> на @role_name
    for role in message.role_mentions:
        quote = re.sub(rf'<@&{role.id}>', f'@{role.name}', quote)
    # Замена упоминаний каналов: <#channel_id> на #channel_name
    for channel in message.channel_mentions:
        quote = re.sub(rf'<#{channel.id}>', f'#{channel.name}', quote)

    # Оборачиваем ссылки на изображения в тексте
    image_extensions = ['png', 'jpg', 'gif', 'jpeg', 'apng', 'webm', 'webp']
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    def is_image_url(url):
        clean_url = re.split(r'[\?#]', url)[0]
        _, ext = os.path.splitext(clean_url.lower())
        return ext[1:] in image_extensions
    parts = []
    last_end = 0
    for match in re.finditer(url_pattern, quote):
        start, end = match.span()
        url = match.group(0)
        parts.append(quote[last_end:start])
        if is_image_url(url):
            parts.append(f'<imgurl={url}>')
        else:
            parts.append(url)
        last_end = end
    parts.append(quote[last_end:])
    quote = ''.join(parts)

    # Инициализация rank и color
    rank = "Discord"
    color = "ffffff"
    color = str(message.author.color).replace("#", "")

    # Инициализация сообщения с quote
    dmessage = quote
    image_count = 0
    for attachment in message.attachments:
        if image_count >= 3:
            break
        attach = attachment.url.split('?')[0]
        if attach.split('.')[-1].lower() in image_extensions:
            # Сокращение ссылки, если длина > 99 символов
            short_url = attachment.url
            if len(short_url) > 99:
                try:
                    response = requests.get(f'http://tinyurl.com/api-create.php?url={short_url}')
                    if response.status_code == 200:
                        short_url = response.text.strip()
                except:
                    pass  # В случае ошибки оставляем оригинальную ссылку

            dmessage += f" <imgurl={short_url}>"
            image_count += 1
    # Нормализация сообщения
    dmessage = unicodedata.normalize('NFKD', dmessage).encode('utf-8', 'ignore').decode("utf-8")
    dname = unicodedata.normalize('NFKD', dname).encode('utf-8', 'ignore').decode("utf-8")
    await compile_send(rank, color, dname, dmessage)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print(' Improper token has been passed.\n Get valid app token https://discord.com/developers/applications/ \nscreenshot http://junger.zzux.com/webhook/guide/valid_token.png')
except discord.HTTPException:
    print(' HTTPException Discord API')
except discord.ConnectionClosed:
    print(' ConnectionClosed Discord API')
except discord.errors.PrivilegedIntentsRequired:
    print(' Privileged Intents Required\n See Privileged Gateway Intents https://discord.com/developers/applications/ \nscreenshot http://junger.zzux.com/webhook/guide/Privileged_Gateway_Intents.png')
	
