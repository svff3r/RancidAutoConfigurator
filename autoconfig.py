#!/usr/bin/env python3
import re
import argparse
from argparse import RawTextHelpFormatter


def get_arguments():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Welcome to Rancid Configuration Creator!',
                                     epilog='Enjoy! =)')

    mutexgroup = parser.add_mutually_exclusive_group(required=True)
    mutexgroup.add_argument('-a', '--add', action='store_true', default=False,
                            help='add new devices.\n'
                                 'You need to fill the following files with the names of the devices you want to add:\n'
                                 '* cisco_list.txt - for Cisco IOS devices\n'
                                 '* fortigate_list.txt - for Fortinet FortiGate devices\n'
                                 '* huawei_list.txt - for Huawei devices (tested only with switches)\n'
                                 '* juniper_list.txt - for Juniper SRX/MX/EX devices\n'
                                 'Each device name should be written on a new line without spaces.')
    mutexgroup.add_argument('-d', '--delete', action='store', default=None, metavar='device_name',
                            help='delete existing device.')
    mutexgroup.add_argument('-r', '--rename', action='store', default=None, nargs=2, metavar=('old_name', 'new_name'),
                            help='rename existing device.')
    return parser.parse_args()


def delete_line(text, file):
    with open(file, "r") as fopen:
        lines = fopen.readlines()
        linescounter = len(lines)
    with open(file, "w") as fopen:
        for line in lines:
            if text not in line:
                linescounter -= 1
                fopen.write(line)
    return linescounter


def find_and_replace(old, new, file):
    with open(file, 'r') as fopen:
        filecontent = fopen.read()
        oldcounter = filecontent.count(old)
        if oldcounter:
            filecontent = filecontent.replace(old, new)
    with open(file, 'w') as fopen:
        fopen.write(filecontent)
    return oldcounter


if get_arguments().add:
    device_counter = 0
    with open('cisco_list.txt', 'r') as cisco_list:
        with open('.cloginrc', 'a') as rancid:
            with open('/usr/local/var/rancid/Cisco/router.db', 'a') as cisco_db:
                for line in cisco_list:
                    if re.match('^[\w-]+$', line):
                        device_counter += 1
                        line = line.rstrip('\n').lower()
                        rancid.write('#' + line + '\n')
                        rancid.write('add user ' + line + ' rancid\n')
                        rancid.write('add method ' + line + ' ssh\n')
                        rancid.write('add password ' + line + ' {Rjyabueh3qiyV3ytl;vtyn}\n')
                        rancid.write('add autoenable ' + line + ' 1\n')
                        rancid.write('\n')
                        line = line.rstrip('\n').upper()
                        cisco_db.write(line + ";cisco;up\n")
    # Erasing 'cisco_list.txt' file:
    cisco_list = open('cisco_list.txt', 'w')
    cisco_list.close()
    print('[+] Added', device_counter, 'Cisco IOS devices')
    device_counter = 0
    with open('fortigate_list.txt', 'r') as fortigate_list:
        with open('.cloginrc', 'a') as rancid:
            with open('/usr/local/var/rancid/FortiGate/router.db', 'a') as fortigate_db:
                for line in fortigate_list:
                    if re.match('^[\w-]+$', line):
                        device_counter += 1
                        line = line.rstrip('\n').lower()
                        rancid.write('#' + line + '\n')
                        rancid.write('add user ' + line + ' fletch\n')
                        rancid.write('add method ' + line + ' ssh\n')
                        rancid.write('add password ' + line + ' pjynbr4Flvby\n')
                        rancid.write('\n')
                        line = line.rstrip('\n').upper()
                        fortigate_db.write(line + ";fortigate;up\n")
    # Erasing 'fortigate_list.txt' file:
    fortigate_list = open('fortigate_list.txt', 'w')
    fortigate_list.close()
    print('[+] Adeed', device_counter, 'Fortinet FortiGate devices')
    device_counter = 0
    with open('huawei_list.txt', 'r') as huawei_list:
        with open('.cloginrc', 'a') as rancid:
            with open('/usr/local/var/rancid/Huawei/router.db', 'a') as huawei_db:
                for line in huawei_list:
                    if re.match('^[\w-]+$', line):
                        device_counter += 1
                        line = line.rstrip('\n').lower()
                        rancid.write('#' + line + '\n')
                        rancid.write('add user ' + line + ' rancid\n')
                        rancid.write('add method ' + line + ' ssh\n')
                        rancid.write('add password ' + line + ' {Rjyabueh3qiyV3ytl;vtyn}\n')
                        rancid.write('add autoenable ' + line + ' 1\n')
                        rancid.write('\n')
                        line = line.rstrip('\n').upper()
                        huawei_db.write(line + ";dit-huawei;up\n")
    # Erasing 'huawei_list.txt' file:
    huawei_list = open('huawei_list.txt', 'w')
    huawei_list.close()
    print('[+] Added', device_counter, 'Huawei devices')
    device_counter = 0
    with open('juniper_list.txt', 'r') as juniper_list:
        with open('.cloginrc', 'a') as rancid:
            with open('/usr/local/var/rancid/Juniper/router.db', 'a') as juniper_db:
                for line in juniper_list:
                    if re.match('^[\w-]+$', line):
                        device_counter += 1
                        line = line.rstrip('\n').lower()
                        rancid.write('#' + line + '\n')
                        rancid.write('add user ' + line + ' fletch\n')
                        rancid.write('add method ' + line + ' ssh\n')
                        rancid.write('add password ' + line + ' pjynbr4Flvby\n')
                        rancid.write('\n')
                        line = line.rstrip('\n').upper()
                        juniper_db.write(line + ";juniper;up\n")
    #Erasing 'juniper_list.txt' file:
    juniper_list = open('juniper_list.txt', 'w')
    juniper_list.close()
    print('[+] Added', device_counter, 'Juniper SRX/MX/EX devices')
    print('\n')
    print('Exiting...')
elif get_arguments().delete:
    device_name = get_arguments().delete
    if re.match('^[\w-]+$', device_name):
        print("[*] File '.cloginrc', deleted",
              delete_line(device_name.lower(), '/home/rancid/.cloginrc'), "line(s)")
        print("[*] File '.../Cisco/router.db', deleted",
              delete_line(device_name.lower(), '/usr/local/var/rancid/Cisco/router.db'), "line(s)")
        print("[*] File '.../FortiGate/router.db', deleted",
              delete_line(device_name.lower(), '/usr/local/var/rancid/FortiGate/router.db'), "line(s)")
        print("[*] File '.../Huawei/router.db', deleted",
              delete_line(device_name.lower(), '/usr/local/var/rancid/Huawei/router.db'), "line(s)")
        print("[*] File '.../Juniper/router.db', deleted",
              delete_line(device_name.lower(), '/usr/local/var/rancid/Juniper/router.db'), "line(s)")
        print('[+] Deleting successful!')
        print('Exiting...')
    else:
        print('[!] Device name seems to be invalid.\n'
              '[!] Please, check the name and try again.')
elif get_arguments().rename:
    (old_name, new_name) = get_arguments().rename
    if re.match('^[\w-]+$', old_name) and re.match('^[\w-]+$', new_name):
        print("[*] File '.cloginrc', found and replaced",
              find_and_replace(old_name.lower(), new_name.lower(), '/home/rancid/.cloginrc'), "entries")
        print("[*] File '.../Cisco/router.db', found and replaced",
              find_and_replace(old_name.lower(), new_name.lower(), '/usr/local/var/rancid/Cisco/router.db'), "entries")
        print("[*] File '.../FortiGate/router.db', found and replaced",
              find_and_replace(old_name.lower(), new_name.lower(), '/usr/local/var/rancid/FortiGate/router.db'), "entries")
        print("[*] File '.../Huawei/router.db', found and replaced",
              find_and_replace(old_name.lower(), new_name.lower(), '/usr/local/var/rancid/Huawei/router.db'), "entries")
        print("[*] File '.../Juniper/router.db', found and replaced",
              find_and_replace(old_name.lower(), new_name.lower(), '/usr/local/var/rancid/Juniper/router.db'), "entries")
        print('[+] Renaming successful!')
        print('Exiting...')
    else:
        print('[!] Device name seems to be invalid.\n'
              '[!] Please, check the name and try again.')
else:
    print("You've broken the program!\nBravo!")