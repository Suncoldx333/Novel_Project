import DiscordBotTest as Bot
import FetchSession
import MJ_Draw as Draw

def loginBot():

    #FetchSession.login(LoginCallback)

    Bot.config_progress_callBack(BotProgressCallBack)
    Bot.config_messsage_callBack(BotRunCallBack)
    Bot.config_message_edit_callBack(BotSingleCallBack)

    Bot.Login(LoginCallback)

def LoginCallback():
    print("BOT READY!")

def BotProgressCallBack(progress):
    print(progress)
    pro = progress[:-1]
    pro_int = int(pro)
    print(pro_int)

def BotRunCallBack(mid, gid, cid, staticSession_id, staticApplication_id,
                   bigArray):
    global messageid, guildid, channelid, sessionid, appid, globalCustomId

    messageid = mid
    guildid = gid
    channelid = cid
    sessionid = staticSession_id
    appid = staticApplication_id
    customid = bigArray[0][0]
    type = 2

    print(f"messageid = {messageid},\nguildid = {guildid},\nchannelis - {channelid},\nsessionid = {sessionid},\nappid = {appid},\ncustomid = {customid}")
    Draw.getMessages()
    #drawCustom(3, type, customid, guildid, channelid, messageid, sessionid, appid) 

def BotSingleCallBack(url):
    print(url)



loginBot()