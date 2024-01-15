sorry for the AI translation

Test version of Cross Chat.
Part for sending Discord messages -> CE.
To work, you need YOUR Discord APP and generate token.
You can obtain it by creating an application here: https://discord.com/developers/applications/
Screen: 🖥️👉 (https://media.discordapp.net/attachments/1117875787601813665/1196265425781149726/0.png)

Upon the first launch, the program will automatically create all the necessary files and prompt you to fill them out (`secur/Token.txt` and `secur/lickey.txt`).

Generate the secret token and write it to **secur\Token.txt**.
**Do not share or transmit your Discord app secret token to anyone!**
Screen: 🖥️👉  (https://media.discordapp.net/attachments/1117875787601813665/1196265426443837540/2.png)

**Important:** Enable intents in the application settings.
Screen: 🖥️👉 (https://media.discordapp.net/attachments/1117875787601813665/1196265426716479498/3.png)

Write the public key (`f3cf1bb45a3878e02eff4d0590974cddc9397ff8860709872b849b51be41aa8c`) to `secur\lickey.txt`.
Screen: 🖥️👉 (https://media.discordapp.net/attachments/665952889755402240/1196266769308975196/image.png)

||
Not mandatory:
If desired, write the IDs of the Discord channels to `secur\Clist.txt` that the application will monitor (only visible in developer mode).
Screen: 🖥️👉 (https://media.discordapp.net/attachments/665952889755402240/1196266999236542484/image.png)
||

**After inviting the bot to your server, a user with administrator permissions can add/remove channels through commands.** For a full list of commands, use /chathelp.
Screen: 🖥️👉 (https://media.discordapp.net/attachments/665952889755402240/1196267204228939886/image.png)

Fill in the `secur\config.ini` file with the servers to which messages from Discord should be sent. The `chat` parameter is optional and defaults to using the PIPPI chat.
For the cautious ones, the config is stored locally and not transmitted to anyone. Access to the RCON port from external addresses can be closed using the standard Windows firewall or opened only for specific IP addresses (stores).

template config.ini
;[shortservname]
;host = address
;port = rcon port
;pass = rcon pass
;chat= (1-PIPPI, 2-AmunatServerTransfer) - chat system message type on server, need installed mod

[exiles]
host = 192.168.0.101
port = 9780
pass = 123456

[siptah]
host = junger.zzux.com
port = 9780
pass = 123456
chat = 2

Inserting images is supported if enabled in the PIPPI chat.
Screens: 🖥️👉 (https://media.discordapp.net/attachments/1117875787601813665/1196271501515706489/image.png) and (https://media.discordapp.net/attachments/1117875787601813665/1196271956249563227/image.png)

If everything is correctly filled in and the keys match, when starting the application, it will provide you with an invitation link for YOUR bot in your Discord server:

`https://discord.com/api/oauth2/authorize?client_id=_DISCORD_APP_ID_&permissions=8&scope=bot`

You can change `permissions=8` to `permissions=0` in the URL to add your Discord application to the server without admin permissions. However, be aware that the application will not be able to see channels with restricted access (private).

The application will automatically add the necessary data to the invitation link. Copy it and paste it into the browser's address bar, where you are logged into Discord.
Screen: 🖥️👉 (https://media.discordapp.net/attachments/1117875787601813665/1196265427811188806/7.png)

During startup, the application makes a request to `http://junger.zzux.com` once to verify the key. In the future, requests are made only to the Discord API. It does not transmit personal, private, secret, or any other data.
**Do not share or transmit your Discord app secret token to anyone!**

To send messages from CE to Discord, use the PIPPI mod or similar mods that have their own webhook server, or use the mechanics previously published to create your own webhook server and send messages to your webhook in your mod.

WINDOWS Binary exe
Download link for on Google Drive: (https://drive.google.com/file/d/1Vx5RaSV1V7tybTTGkOo3d1rpL6j8Lqws/view?usp=sharing)
VirusTotal: (https://www.virustotal.com/gui/file-analysis/YTk3MmYwZmVkOGVlNGJhZjA3Zjk4YWZmZTU1ZWEwOWE6MTcwNTI4NTIzNQ==)
