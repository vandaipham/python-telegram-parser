import os, sys
import time


re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"


def requirements():
    print("Installing requiremnts.....")
    os.system('''
        pip3 install -r requirements.txt
        touch config.data
        ''')
    print("Requirments installed")

def config_setup():
    import configparser
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(gr+"[+] enter api ID : "+re)
    cpass.set('cred', 'id', xid)
    xhash = input(gr+"[+] enter hash ID : "+re)
    cpass.set('cred', 'hash', xhash)
    xphone = input(gr+"[+] enter phone number : "+re)
    cpass.set('cred', 'phone', xphone)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    print(gr+"[+] setup complete !")


if __name__ == '__main__':
    requirements()
    config_setup()