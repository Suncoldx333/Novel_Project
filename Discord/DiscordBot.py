#import DiscordBotTest as Bot
#import FetchSession
#import MJ_Draw as Draw

import DiscordBotLoginMode as LoginMode
import Discord_Const as Const
import threading

loginCallBack_g = None
progressCallBack_g = None

def loginBot(callback):
    Const.log("BOT LOGIN")
    global loginCallBack_g
    loginCallBack_g = callback
    signid = "123"
    thread = threading.Thread(target=threadLoginBot,args=(signid,LoginCallback))
    thread.start()

def threadLoginBot(signid,callback):
    LoginMode.config_progress_callBack(BotProgressCallBack)
    LoginMode.Login(callback)

def LoginCallback(success,sessionid):
    global loginCallBack_g
    if loginCallBack_g:
        loginCallBack_g(success,sessionid)

def configProgressCallBack(callback):
    Const.log("123")
    global progressCallBack_g
    progressCallBack_g = callback

def BotProgressCallBack(progress):
    print(progress)
    pro = progress[:-1]
    pro_int = int(pro)
    print(pro_int)
    global progressCallBack_g
    progressCallBack_g(200,pro_int)

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
    #Draw.getMessages()
    #drawCustom(3, type, customid, guildid, channelid, messageid, sessionid, appid) 

def BotSingleCallBack(url):
    print(url)



#loginBot()