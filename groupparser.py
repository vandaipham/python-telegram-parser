import datetime
from typing import List
import requests
from bs4 import BeautifulSoup
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


def getGroupList(telegamClient) -> List:
    '''
    Turns a list of Telegram Mega or Giga Groups

        Parameters:
            telegramClient (Entity): A telegram client Entity

        Returns:
            groups (List): A list of mega or giga groups.
    '''
    groups = []
    chats = []
    # GET all dialogs
    result = telegamClient(GetDialogsRequest(
             offset_date=datetime.datetime.now(),
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=200,
             hash = 0
         ))
    chats.extend(result.chats)
 
    for chat in chats:
        try:
            if (chat.megagroup==True) or (chat.gigagroup==True):
                groups.append(chat)
        except:
            continue
    return groups


def getGroupLinks(file) -> List:
    '''
    This function reads an input file and returns a list of links.

        Parameters:
            file (string): A file path

        Returns:
            groupLinks (list): List of group links
    '''
    groupLinks = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            groupLinks.append(line.strip())
    return groupLinks


def getGroupEntity(telegramClient, groupLink):
    '''
    This function is used to get the telegram group Entity.

        Parameters:
            telegramClient (EntityLike): A telegram client object
            groupLink: A telegram group link or invited link

        Returns:
            Entity of the telegram group
    '''
    try:
        # if group is open
        return telegramClient.get_entity(groupLink)
    except:
        # if group is private
        r = requests.get(groupLink)
        soup = BeautifulSoup(r.text, 'html.parser')
        groupTag = soup.find("meta", attrs={"property": "og:title"})
        groupName = groupTag['content']
        try:
            return telegramClient.get_entity(groupName)
        except:
            return None


def getGroupPosts(telegramClient, groupLink: str, timeFrom: datetime, timeNow: datetime) -> List:
    '''
    This functions turns a list of all users' post in the group

        Parameters:
            telegramClient (Entity): A telegram client Entity
            groupLink (str): A group link or invited link for a private group
            timeFrom (datetime): The start parsed time
            timeNow (datetime): The time now
        
        Returns:
            msgDict (List): A list of posts in the group
    '''
    msgDict = []
    try:
        groupEntity = getGroupEntity(telegramClient, groupLink)
        msgArr = [] # this arrary is used to save all message from_date to timeNow
        minID = 0
        maxID = 0
        myDict = {'groupLink':'', 'username':'', 'userID': '', 'date':'', 'message':''}
        lastMsgArr = telegramClient.get_messages(groupEntity, offset_date=timeNow, limit=10)
        if len(lastMsgArr) > 0:
            for i in range(0, len(lastMsgArr)):
                if (lastMsgArr[i].text != None) and (lastMsgArr[i].sender_id != None) :
                    if (lastMsgArr[i].date + datetime.timedelta(hours=3)).timestamp() < timeFrom.timestamp():
                        print("There is no message found at the last time")
                    else:
                        msgArr.append(lastMsgArr[i])    # add the last message to msgArr
                        maxID = lastMsgArr[i].id
                    break

        if len(msgArr) > 0:
            # Get the minID of the message in the group
            firstMsgArr = telegramClient.get_messages(groupEntity, offset_date=timeFrom-datetime.timedelta(hours=3), limit=1)
            minID = firstMsgArr[0].id
            
            # Get all messages from minID to maxID:
            allMsg = telegramClient.get_messages(groupEntity, max_id=maxID, min_id=minID)
            msgArr.extend(allMsg)
            # Processing message array
            for msgEntity in msgArr:
                if (msgEntity.text != None) and ((msgEntity.date + datetime.timedelta(hours=3)).timestamp() >= timeFrom.timestamp()) and (msgEntity.sender_id != None):
                    if (msgEntity.sender):
                        username = msgArr[i].sender.username
                    else:
                        username = ""
                    myDict = {'groupLink':'', 'username':'', 'userID': '', 'date':'', 'message':''}
                    myDict['groupLink'] = groupLink
                    myDict['username'] = username
                    myDict['userID'] = msgEntity.sender_id
                    myDict['date'] = msgEntity.date + datetime.timedelta(hours=3)
                    myDict['message'] = str(msgEntity.text).replace("\n", " ")
                    msgDict.append(myDict)
        return msgDict

    except:
        print("The group link " + groupLink + " is not found")
        return msgDict