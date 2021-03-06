#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam
# @Data     : 2021-06-15
# @Version  : v 2.5
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, logger, api_id, api_hash, proxystart, proxy, _ScriptsDir, _OwnDir, _JdbotDir, TOKEN
from ..bot.utils import cmd, press_event, backfile, jdcmd, _DiyDir, V4, QL, _ConfigFile, myck
from telethon import events, TelegramClient, Button
import re, json, requests, os, asyncio,time,datetime


if proxystart:
    client = TelegramClient("user", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("user", api_id, api_hash, connection_retries=None).start()


with open(f"{_ConfigDir}/diybotset.json", 'r', encoding='utf-8') as f:
    diybotset = json.load(f)
my_chat_id = int(diybotset['my_chat_id'])


bot_id = int(TOKEN.split(':')[0])


def checkCookie1():
    expired = []
    cookies = myck(_ConfigFile)
    for cookie in cookies:
        cknum = cookies.index(cookie) + 1
        if checkCookie2(cookie):
            expired.append(cknum)
    return expired, cookies


def checkCookie2(cookie):
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = requests.get(url, headers=headers).json()
        if r['retcode'] == '1001':
            return True
        else:
            return False
    except:
        return False


def getbean(i, cookie, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie,
    }
    result, o = '', '\n\t\t???'
    try:
        r = requests.get(url=url, headers=headers)
        res = r.json()
        if res['code'] == '0':
            followDesc = res['result']['followDesc']
            if followDesc.find('??????') != -1:
                try:
                    for n in range(len(res['result']['alreadyReceivedGifts'])):
                        redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                        rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                        result += f"{o}?????????????????????{redWord}{rearWord}"
                except:
                    giftsToast = res['result']['giftsToast'].split(' \n ')[1]
                    result = f"{o}{giftsToast}"
            elif followDesc.find('??????') != -1:
                result = f"{o}{followDesc}"
        else:
            result = f"{o}Cookie ??????????????????"
    except Exception as e:
        if str(e).find('(char 0)') != -1:
            result = f"{o}??????????????????????????????????????????"
        else:
            result = f"{o}?????????????????????{e}"
    return f"\n????????????{i}{result}\n"


# user?
@client.on(events.NewMessage(chats=[bot_id, my_chat_id], from_users=chat_id, pattern=r"^user(\?|\???)$"))
async def fortest(event):
    try:
        msg = await jdbot.send_message(chat_id, '??????,??????...')
        await asyncio.sleep(5)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@client.on(events.NewMessage(chats=[-1001197524983,my_chat_id], pattern=r'.*???'))
async def shopbean(event):
    cookies = myck(_ConfigFile)
    message = event.message.text
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message)
    if url != [] and len(cookies) > 0:
        i = 0
        info = '????????????\n' + message.split("\n")[0] + "\n"
        for cookie in cookies:
            try:
                i += 1
                info += getbean(i, cookie, url[0])
            except:
                continue
        await jdbot.send_message(chat_id, info)


@client.on(events.NewMessage(chats=[-1001419355450,-1001284907085,-1001320212725, my_chat_id]))
async def zoo_shopbean(event):
    cookies = myck(_ConfigFile)
    message = event.message.text
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message)
    if url != [] and len(cookies) > 0:
        i = 0
        info = '????????????\n' + "\n"
        for cookie in cookies:
            try:
                i += 1
                info += getbean(i, cookie, url[0])
            except:
                continue
        if '??????' in info:
            await jdbot.send_message(chat_id, '???????????????????????????????????????????????????!')
        else:
            await jdbot.send_message(chat_id, '?????????????????????!')

@client.on(events.NewMessage(chats=[-1001370656674,-1001320212725,my_chat_id], pattern=r"^export jd_zdjr_.*=\".*\"|^export jd_joinTeam_activityId.*=\".*\"|^export OPEN_CARD_.*=\".*\"|^export FAV_.*=\".*\"|^export ISV_.*=\".*\""))
async def myexport(event):
    try:
        messages = event.message.text.split("\n")
        identity=''
        msg = await jdbot.send_message(chat_id, "????????????????????????????????????????????????")
        end = ''
        for message in messages:
            if "joinTeam" in message:
                identity = "??????2"
            elif "OPEN_CARD" in message:
                identity = "??????"
            elif "FAV_" in message:
                identity = "????????????"
            elif "ISV_" in message:
                identity = "????????????"
            elif "jd_zdjr" in message:
                identity = "??????1"
            kv = message.replace("export ", "").replace("*", "")
            kname = kv.split("=")[0]
            vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            if kv in configs:
                continue
            if "jd_zdjr" in message and len(vname) != 32:
                msg = await jdbot.edit_message(msg, f"?????????????{identity}???????????????????????????????????????")
                return
            if configs.find(kname) != -1:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"??????{identity}??????????????????"
            else:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("????????????") != -1 and config.find("???") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 2, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"??????{identity}??????????????????"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if len(end) == 0:
            await jdbot.edit_message(msg, f"?????????{identity}?????????????????????????????????!")
            return
        await jdbot.edit_message(msg, end)
        if "??????2" in identity:
            await cmd("sh /jd/config/gua_joinTeam.sh")
        elif "??????" in identity:
            await cmd('sh /jd/config/jd_open_card_by_shopid.sh')
        elif "????????????" in identity:
            await cmd('sh /jd/config/jd_fav_shop_gift.sh')
        elif "????????????" in identity:
            await cmd('sh /jd/config/jd_follow_wxshop_gift_lof.sh')            
        elif "??????1" in identity:
            await cmd("sh /jd/config/smiek_jd_zdjr.sh")
        else:
            await jdbot.edit_message(msg, f"???????????????,????????????BUG!")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


        
@client.on(events.NewMessage(chats=[-1001159808620, my_chat_id], pattern=r".*?????????.*"))
async def redrain(event):
    try:
        if V4:
            if not os.path.exists('/jd/config/jredrain.sh'):
                cmdtext = 'cd /jd/config && wget https://raw.githubusercontent.com/chiupam/JD_Diy/master/pys/jredrain.sh'
                await cmd(cmdtext)
        else:
            if not os.path.exists('/ql/jredrain.sh'):
                cmdtext = 'cd /ql && wget https://raw.githubusercontent.com/chiupam/JD_Diy/master/pys/jredrain.sh'
                await cmd(cmdtext)
        message = event.message.text
        RRAs = re.findall(r'RRA.*', message)
        Times = re.findall(r'????????????.*', message)
        for RRA in RRAs:
            i = RRAs.index(RRA)
            if V4:
                cmdtext = f'/cmd bash /jd/config/jredrain.sh {RRA}'
            else:
                cmdtext = f'/cmd bash /ql/jredrain.sh {RRA}'
            Time_1 = Times[i].split(" ")[0].split("-")
            Time_2 = Times[i].split(" ")[1].split(":")
            Time_3 = time.localtime()
            year, mon, mday = Time_3[0], Time_3[1], Time_3[2]
            await client.send_message(bot_id, cmdtext, schedule=datetime.datetime(year, int(Time_1[1]), int(Time_1[2]), int(Time_2[0]) - 8 , int(Time_2[1]), 0, 0))
            end = f'??????????????????\n{Times}\n??????:{RRA}'
            end = end.replace("[","").replace("\'","").replace("]","")
            await jdbot.send_message(chat_id, end)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))

# -100123456789 ????????????id???????????????????????????1????????????????????????????????????????????????????????????????????????1???id
@client.on(events.NewMessage(chats=-1001175133767))
async def myforward(event):
    try:
        # -100123456789 ????????????id???????????????????????????1????????????????????????????????????????????????????????????????????????1???id
        await client.forward_messages(bot_id, event.id, -1001175133767)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))



@client.on(events.NewMessage(chats=[-1001419355450, my_chat_id], pattern=r"^#??????"))
async def myzoo(event):
    """
    ???????????????
    ???????????????https://t.me/zoo_channel
    """
    try:
        messages = event.message.text
        url = re.findall(re.compile(r"[(](https://raw\.githubusercontent\.com.*?)[)]", re.S), messages)
        if url == []:
            return
        else:
            url = url[0]
        speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
        for speed in speeds:
            resp = requests.get(f"{speed}{url}").text
            if resp:
                break
        if resp:
            fname = url.split('/')[-1]
            fname_cn = re.findall(r"(?<=new\sEnv\(').*(?=')", resp, re.M)
            if fname_cn != []:
                fname_cn = fname_cn[0]
            else:
                fname_cn = ''
            fpath = f"{_ScriptsDir}/{fname}"
            backfile(fpath)
            with open(fpath, 'w+', encoding='utf-8') as f:
                f.write(resp)
            cmdtext = False
            try:
                with open(f"{_ConfigDir}/diybotset.json", 'r', encoding='utf-8') as f:
                    diybotset = json.load(f)
                run = diybotset['zoo??????????????????']
            except:
                btns = [Button.inline("???", data="confirm"), Button.inline("???", data="no"), Button.inline("????????????", data="cancel")]
                async with jdbot.conversation(int(chat_id), timeout=60) as conv:
                    msg = await jdbot.send_message(chat_id, f"???????????????????????????????????????????????????????????????", buttons=btns)
                    convdata = await conv.wait_event(press_event(int(chat_id)))
                    res = bytes.decode(convdata.data)
                    if res == "cancel":
                        await jdbot.edit_message(msg, '????????????????????????????????????')
                        conv.cancel()
                        return
                    elif res == "no":
                        run = 'False'
                    else:
                        run = 'True'
                    await jdbot.edit_message(msg, "????????????")
                    conv.cancel()
                with open(f"{_ConfigDir}/diybotset.json", 'r', encoding='utf-8') as f1:
                    diybotsets = f1.readlines()
                diybotsets[-2] = diybotsets[-2][:-1]+',\n'
                diybotsets.insert(-1, f'  "zoo??????????????????": "{run}"\n')
                with open(f"{_ConfigDir}/diybotset.json", 'w', encoding='utf-8') as f2:
                    f2.write(''.join(diybotsets))
            if run == "False":
                await jdbot.send_message(chat_id, f"????????????????????????{_ScriptsDir}??????\n??????????????????config??????diybotset.json????????????Ture")
            else:
                cmdtext = f'{jdcmd} {fpath} now'
                await jdbot.send_message(chat_id, f"????????????????????????{_ScriptsDir}??????\n?????????????????????config??????diybotset.json????????????False")
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, f'?????????????????????????????????\n??????????????????????????????\n```/cmd {jdcmd} {fpath} now```')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
# @client.on(events.NewMessage(chats=[-1001431256850, my_chat_id], from_users=1185488678))
# async def myupuser(event):
#     """
#     ???????????????https://t.me/jd_diy_bot_channel
#     """
#     try:
#         if event.message.file:
#             fname = event.message.file.name
#             try:
#                 if fname.endswith("bot-06-21.py") or fname.endswith("user.py"):
#                     path = f'{_JdbotDir}/diy/{fname}'
#                     backfile(path)
#                     await client.download_file(input_location=event.message, file=path)
#                     from ..diy.bot import restart
#                     await restart()
#             except:
#                 return
#     except Exception as e:
#         await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
#         logger.error('something wrong,I\'m sorry\n' + str(e))


