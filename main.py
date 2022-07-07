import csv
import datetime
import groupparser
import configparser
from telethon.sync import TelegramClient
import os, sys


def main():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')

    try:
        api_id = cpass['cred']['id']
        api_hash = cpass['cred']['hash']
        phone = cpass['cred']['phone']
        client = TelegramClient(phone, api_id, api_hash)
    except KeyError:
        os.system('clear')
        print("run pip install -r requirments.txt !!\n")
        sys.exit(1)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        os.system('clear')
        client.sign_in(phone, input('[+] Enter the code: '))
 
    os.system('clear')

    # Get number of hours from user
    print("Welcome to paser!!!!\n")
    numberOfHours = input("Enter a Number of Parsing Hours: ")
    print("-----------------")
    timeNow = datetime.datetime.now()
    print("Time now: ", timeNow)
    timeFrom = timeNow - datetime.timedelta(hours=int(numberOfHours))
    print("Parsing messages from: ", timeFrom)
    print("***")

    # Create a file to save the parsed posts
    dataFile = open("data.csv", "w")
    keys = ['groupLink', 'username', 'userID', 'date', 'message']
    dict_writer = csv.DictWriter(dataFile, keys)

    groupLinks = groupparser.getGroupLinks('groupList.txt')
    print(groupLinks)
    for groupLink in groupLinks:
        print("Start parsing the group " + groupLink)
        results = groupparser.getGroupPosts(client, groupLink, timeFrom, timeNow)
        dict_writer.writerows(results)
        print("Finish parsing the group " + groupLink)
        print("-------------------------------------")
    dataFile.close()
        

if __name__ == '__main__':
    main()