import requests

import time
from colorama import init, Fore, Style
import sys
import os
import get_query_id
init(autoreset=True)
import requests



def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        print(tokens)
        return tokens
    except FileNotFoundError:
        print("Không tìm thấy file query.txt")
        return [  ]
    except Exception as e:
        print("Đã xảy ra lỗi:", str(e))
        return [  ]

import datetime
import pytz

def check_worm():
    response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
    if response.status_code == 200:
        worm_data = response.json().get('data', {})
        next_refresh = worm_data.get('next_refresh')
        is_caught = worm_data.get('is_caught')

        if next_refresh is not None and is_caught is not None:
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)

            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)

            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Tiếp theo trong {hours} giờ {minutes} phút - Trạng thái: {'Đã bắt' if is_caught else 'Có sẵn'}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Dữ liệu worm không đầy đủ")

        return worm_data
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Không lấy được dữ liệu.")
        return None
def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data['is_caught']:
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Bắt sâu thành công")
        elif response.status_code == 400:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Đã bắt sâu")
        elif response.status_code == 404:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Không tìm thấy sâu")    
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Không bắt được sâu, mã trạng thái:", response)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Sâu không có sẵn hoặc đã bắt.")


def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ {name} ] ==============")
        upgrades = {}
        for upgrade in profile_data['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            if upgrade_type in upgrades:
                if upgrade_level > upgrades[upgrade_type]:
                    upgrades[upgrade_type] = upgrade_level
            else:
                upgrades[upgrade_type] = upgrade_level

        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
        return profile_data
    else:
        print("Không lấy được dữ liệu, mã trạng thái:", response.status_code)
        return None 

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance_data[ 'data' ] / 1000000000}")
        return True  
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Thất bại |{response.status_code}")
        return False

def checkin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        data = response.json()
        day = data.get('data', {}).get('no', '')
        print(f"{Fore.GREEN+Style.BRIGHT}[ Checkin ]: Điểm danh thành công | Ngày {day}")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED+Style.BRIGHT}[ Checkin ]: Đã điểm danh hôm nay")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Checkin ]: Thất bại | {data}")
        

def upgrade_storage():
    confirm = input("Bạn có muốn nâng cấp storage không? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade storage ]: Thành công'
        else:
            return '[ Upgrade storage ]: Số dư không đủ'
    else:
        return None

def upgrade_mining():
    confirm = input("Bạn có muốn nâng cấp mining không? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade mining ]: Thành công'
        else:
            return '[ Upgrade mining ]: Số dư không đủ'
    else:
        return None

def upgrade_holy():
    confirm = input("Bạn có muốn nâng cấp holy không? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade holy ]: Thành công'
        else:
            return '[ Upgrade holy ]: Điều kiện không đủ'
    else:
        return None
def upgrade_storage(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_storage, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade storage ]: Thành công'
        else:
            return '[ Upgrade storage ]: Số dư không đủ'
    else:
        return None

def upgrade_mining(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_mining, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade mining ]: Thành công'
        else:
            return '[ Upgrade mining ]: Số dư không đủ'
    else:
        return None
def upgrade_holy(confirm):
    if confirm.lower() == 'y':
        response = requests.post(url_upgrade_holy, headers=headers)
        if response.status_code == 200:
            return '[ Upgrade holy ]: Thành công'
        else:
            return '[ Upgrade holy ]: Điều kiện không đủ'
    else:
        return None
def get_tasks():
    
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)

    tasks = response.json()['data']
    
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            complete_task(task['id'],task['name'])

def complete_task(task_id,task_name):
   
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tasks ]: Nhiệm vụ {task_name} đã hoàn thành.")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tasks ]: Không thể hoàn thành nhiệm vụ {task_name}, mã trạng thái: {response.status_code}")


def main():
    confirm_storage = input("Tự động nâng cấp storage? (y/n): ")
    confirm_mining = input("Tự động nâng cấp mining? (y/n): ")
    confirm_holy = input("Tự động nâng cấp holy? (y/n): ")
    confirm_task = input("Tự động hoàn thành nhiệm vụ? (y/n): ")
    while True:
        tokens = load_credentials()
        hasil_upgrade = upgrade_storage(confirm_storage)
        hasil_upgrade1 = upgrade_mining(confirm_mining)
        hasil_upgrade2 = upgrade_holy(confirm_holy)
        break_current_loop = False
        for index, token in enumerate(tokens):
            headers[ 'telegram-data' ] = token
            info = get_profile()
            if info is None: 
                print(f"{Fore.RED+Style.BRIGHT}[ Token ]: Làm mới token")
                get_query_id.run()
                print(f"{Fore.GREEN+Style.BRIGHT}[ query_id ]: Lấy token mới thành công")
                break_current_loop = True
                break
            if info:
                print(f"Đang xử lý tài khoản {info[ 'data' ][ 'name' ]}")
                
            if hasil_upgrade:
                print(hasil_upgrade)
                time.sleep(1)  
            if hasil_upgrade1:
                print(hasil_upgrade1) 
                time.sleep(1)
            if hasil_upgrade2:
                print(hasil_upgrade2)
                time.sleep(1)

            if check_balance():
                response = requests.post(url_claim, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Claim thành công")
                elif response.status_code == 400:
                    response_data = response.json()
                    print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Chưa đến giờ claim")
                else:
                    print("Đã xảy ra lỗi, mã trạng thái:", response.status_code)

                checkin_daily()
                catch_worm()
                if confirm_task.lower() == 'y':
                    get_tasks()

        if break_current_loop == False:
            for i in range(300, 0, -1):
                sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Đã xử lý hết tài khoản, đợi {i} giây trước khi tiếp tục vòng lặp ============")
                sys.stdout.flush()
                time.sleep(1)
        print()
        clear_console()

        
if __name__ == "__main__":
    main()
