import requests
import json
import os
import random
import urllib.parse
from colorama import *
from datetime import datetime, timezone
import time
import pytz

wib = pytz.timezone("Asia/Jakarta")

class Wonton:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Host": "wonton.food",
            "Origin": "https://www.wonton.restaurant",
            "Pragma": "no-cache",
            "Referer": "https://www.wonton.restaurant/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
        self.base_url = "https://wonton.food/api/v1"

    def clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Wonton - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get("user", [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            user_id = user_data["id"]
            return user_id
        else:
            raise ValueError("User data not found in query.")

    def user_auth(self, query: str, retries=5):
        url = f"{self.base_url}/user/auth"
        data = json.dumps({"initData":query, "inviteCode":"XE9DB2JV", "newUserPromoteCode":""})
        self.headers.update({
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()['tokens']['accessToken']
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def user_data(self, token: str, retries=5):
        url = f"{self.base_url}/user"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def claim_gift(self, token: str, retries=5):
        url = f"{self.base_url}/user/claim-gift"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 403:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reason{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Join Wonton's Channel First {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    return
                
                elif response.status_code == 500:
                    return None
                
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def check_in(self, token: str, retries=5):
        url = f"{self.base_url}/checkin"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def claim_refferal(self, token: str, retries=5):
        url = f"{self.base_url}/invite/claim-progress"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers)
                response.raise_for_status()
                return response.json()['items']
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def farming_status(self, token: str, retries=5):
        url = f"{self.base_url}/user/farming-status"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def start_farming(self, token: str, retries=5):
        url = f"{self.base_url}/user/start-farming"
        data = {}
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def claim_farming(self, token: str, retries=5):
        url = f"{self.base_url}/user/farming-claim"
        data = {}
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def user_blindbox(self, token: str, retries=5):
        url = f"{self.base_url}/shop/user-blindbox"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def purchase_basicbox(self, token: str, amount: int, retries=5):
        url = f"{self.base_url}/shop/purchase-basic-box"
        data = json.dumps({"purchaseAmount":amount})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return True
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def draw_basicbox(self, token: str, draw_amount: int, retries=5):
        url = f"{self.base_url}/shop/draw-basic-box"
        data = json.dumps({"drawAmount":draw_amount})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def badge_list(self, token: str, retries=5):
        url = f"{self.base_url}/badge/list"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()['badges']
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def claim_badge(self, token: str, type: str, retries=5):
        url = f"{self.base_url}/badge/claim"
        data = json.dumps({"type":type})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def start_game(self, token: str, retries=5):
        url = f"{self.base_url}/user/start-game"
        data = {}
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def finish_game(self, token: str, points: int, bonus: bool, retries=5):
        url = f"{self.base_url}/user/finish-game"
        data = json.dumps({"points":points, "hasBonus":bonus})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}               ",
                        end="\r",
                        flush=True
                    )
                    time.sleep(5)
                else:
                    return None
                
    def skins_list(self, token: str, retries=5):
        url = f'{self.base_url}/shop/list'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()['shopItems']
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def use_skins(self, token: str, skin_id: int, retries=5):
        url = f'{self.base_url}/shop/use-item'
        data = json.dumps({'itemId':skin_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return True
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def items_list(self, token: str, retries=5):
        url = f"{self.base_url}/shop/fusion-items/list"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def fuse_items(self, token: str, fusion_id: str, retries=5):
        url = f"{self.base_url}/shop/fuse-item"
        data = json.dumps({"fusionId": fusion_id})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                if response.status_code == 400:
                    return None

                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def special_tasks(self, token: str, type: str, retries=5):
        url = f"{self.base_url}/user/claim-task-gift?type={type}"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 400:
                    return None

                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def tasks(self, token: str, retries=5):
        url = f"{self.base_url}/task/list"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def start_tasks(self, token: str, task_id: str, retries=5):
        url = f"{self.base_url}/task/verify"
        data = json.dumps({"taskId":task_id})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                if response.status_code == 400:
                    return False

                response.raise_for_status()
                return True
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def claim_tasks(self, token: str, task_id: str, retries=5):
        url = f"{self.base_url}/task/claim"
        data = json.dumps({"taskId":task_id})
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                if response.status_code == 400:
                    return False

                response.raise_for_status()
                return True
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
    
    def claim_progress_tasks(self, token: str, retries=5):
        url = f"{self.base_url}/task/claim-progress"
        self.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def calculate_balance(self, queries):
        total_wton = 0
        total_ton = 0
        total_usdt = 0

        for query in queries:
            query = query.strip()
            if query:
                token = self.user_auth(query)
                if token:
                    user = self.user_data(token)
                    skins = self.skins_list(token)
                    if user and skins:
                        total_wton += float(user['tokenBalance'])
                        total_ton += sum(float(item["value"]) * item["inventory"] for item in skins if item["sellToken"] == 0)
                        total_usdt += sum(float(item["value"]) * item["inventory"] for item in skins if item["sellToken"] == 1)

        return total_wton, total_ton, total_usdt
                
    def question(self):
        while True:
            purchase_box = input("Auto Purchase & Open Basic Box? [y/n] -> ").strip().lower()
            if purchase_box in ["y", "n"]:
                purchase_box = purchase_box == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to purchase or 'n' to skip.{Style.RESET_ALL}")

        return purchase_box
    
    def process_query(self, query: str, purchase_box: bool):

        token = self.user_auth(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Query Id May Expired {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if token:
            user = self.user_data(token)
            if not user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Query Id May Expired {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                return
            
            if user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['tokenBalance']} $WTON {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['withdrawableBalance']} $TON {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['withdrawableUSDTBalance']} $USDT {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                time.sleep(1)

                gift = self.claim_gift(token)
                if gift:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Gift{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} 1 Skins {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                check_in = self.check_in(token)
                if check_in and check_in['newCheckin']:
                    reward = next((config for config in check_in['configs'] if config['day'] == check_in['lastCheckinDay']), None)
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {reward['tokenReward']} $WTON {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {reward['ticketReward']} Ticket {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                claim_reff = self.claim_refferal(token)
                if claim_reff:
                    if isinstance(claim_reff, list) and len(claim_reff) > 0:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {len(claim_reff)} Skins {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} No Available Reward to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} No Available Reward to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                farming = self.farming_status(token)
                if farming == {}:
                    start = self.start_farming(token)
                    if start:
                        claim_time = datetime.strptime(start['finishAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                        claim_time_wib = claim_time.astimezone(wib).strftime('%x %X %Z')
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {claim_time_wib} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    
                elif farming != {}:
                    claimed = farming['claimed']
                    if not claimed:
                        claim_at = datetime.strptime(farming['finishAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                        now = datetime.now(timezone.utc)
                        claim_at_wib = claim_at.astimezone(wib).strftime('%x %X %Z')

                        if now >= claim_at:
                            claim = self.claim_farming(token)
                            if claim and claim['claimed']:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {farming['totalAmount']} $WTON {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                                time.sleep(1)

                                start = self.start_farming(token)
                                if start:
                                    claim_time = datetime.strptime(start['finishAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                                    claim_time_wib = claim_time.astimezone(wib).strftime('%x %X %Z')
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {claim_time_wib} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {claim_at_wib} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        start = self.start_farming(token)
                        if start:
                            claim_time = datetime.strptime(start['finishAt'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
                            claim_time_wib = claim_time.astimezone(wib).strftime('%x %X %Z')
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {claim_time_wib} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                if purchase_box:
                    blindbox = self.user_blindbox(token)
                    if blindbox:
                        amount = blindbox.get('basicBoxQuota', {}).get('available', None)
                        price = blindbox.get('blindbox', {}).get('basicBox', {}).get('price', None)
                        total_price = price * amount
                        balance = int(self.user_data(token)['tokenBalance'])

                        if amount > 0:
                            if balance >= total_price:
                                purchase = self.purchase_basicbox(token, amount)
                                if purchase:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT} Is Purchased {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Amount{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {amount} Box {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                    time.sleep(1)

                                    if amount in [1, 2, 3]:
                                        draw_amounts = [amount]
                                    elif amount == 4:
                                        draw_amounts = [3, 1]
                                    elif amount == 5:
                                        draw_amounts = [3, 2]
                                    elif amount == 6:
                                        draw_amounts = [3, 3]
                                    else:
                                        draw_amounts = []

                                    for draw_amount in draw_amounts:
                                        draw = self.draw_basicbox(token, draw_amount)
                                        if draw:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                                f"{Fore.GREEN+Style.BRIGHT} Is Opened{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                                f"{Fore.WHITE+Style.BRIGHT} {draw_amount} Skins {Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                            )
                                        else:
                                            self.log(
                                                f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                                f"{Fore.RED+Style.BRIGHT} Isn't Opened{Style.RESET_ALL}"
                                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                            )
                                        time.sleep(1)

                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Isn't Purchased{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT} Isn't Purchased{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} $WTON Not Enough {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Isn't Purchased{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reason{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} No Available {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Basic Box{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Skipping to Purchase {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                badge_list = self.badge_list(token)
                if badge_list:
                    while True:
                        has_claimed = False
                        for type, badge in badge_list.items():
                            progress = badge['progress']
                            target = badge['target']

                            if progress is None:
                                continue

                            progress = int(progress)
                            target = int(target)

                            while progress >= target:
                                claim = self.claim_badge(token, int(type))
                                if claim:
                                    reward_mapping = {
                                        'tickets': 'Ticket',
                                        'silverPacks': 'Skins',
                                        'bowls': 'Bowls',
                                        'tokens': '$WTON',
                                    }
                                    rewards = []
                                    for reward_type, amount in zip(badge['rewardTypes'], badge['rewardDetails']):
                                        if amount > 0:
                                            rewards.append(f"{amount} {reward_mapping[reward_type]}")

                                    reward = ", ".join(rewards)

                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Badge{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {badge['name']} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} Level {badge['level']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {reward} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                    has_claimed = True
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Badge{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {badge['name']} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} Level {badge['level']} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reason{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} Not Eligible {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                    break

                                time.sleep(1)

                                badge_list = self.badge_list(token)
                                badge = badge_list.get(str(type))
                                if not badge:
                                    break

                                progress = badge['progress']
                                target = badge['target']
                                if progress is None:
                                    break

                                progress = int(progress)
                                target = int(target)

                        if not has_claimed:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Badge{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} No Available to Claim {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                            break
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Badge{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                tickets = self.user_data(token)['ticketCount']
                if tickets > 0:
                    while tickets > 0:
                        start = self.start_game(token)
                        if start:
                            tickets -= 1
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Ticket{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {tickets} Left {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )

                            for remaining in range(random.randint(15, 20), 0, -1):
                                print(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}Seconds to Complete Game{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                                    end="\r",
                                    flush=True
                                )
                                time.sleep(1)

                            points = random.randint(900, 925)
                            bonus = start.get('bonusRound', False)
                            claim = self.finish_game(token, points, bonus)
                            if claim:
                                bonus = claim.get('items', [])
                                reward = len(bonus) if len(bonus) > 0 else 0
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {points} $WTON {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {reward} Skins {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} Isn't Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                        "
                                )
                            time.sleep(1)

                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}               "
                            )
                            break

                    if tickets == 0:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} No Available Tickets {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} No Available Tickets {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                skins = self.skins_list(token)
                if skins:
                    valid_skins = [skin for skin in skins if int(skin['inventory']) > 0]
                    if valid_skins:
                        greatest_power = max(valid_skins, key=lambda skin: int(skin['farmingPower']))
            
                        skin_id = greatest_power['id']
                        in_use = greatest_power['inUse']

                        if not in_use:
                            use = self.use_skins(token, skin_id)
                            if use:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {greatest_power['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Success to Use{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Farming Power{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {greatest_power['farmingPower']} $WTON/3hours {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {greatest_power['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Is Failed to Use{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {greatest_power['name']} {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}Is Already in Use{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Farming Power{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {greatest_power['farmingPower']} $WTON/3hours {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} No Have Skin Yet {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                fusions = self.items_list(token)
                if fusions:
                    for fusion in fusions['items']:
                        fusion_id = fusion['id']

                        if fusion:
                            fuse = self.fuse_items(token, fusion_id)
                            if fuse:
                                reward_value = fusion['shopItem']['value']
                                reward_type = '$USDT' if fusion['shopItem']['sellToken'] == 1 else '$TON'
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Fusion Skins{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {fusion['shopItem']['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Success{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {reward_value} {reward_type} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Fusion Skins{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {fusion['shopItem']['name']} {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Isn't Success{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reason{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} Not Eligible {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            time.sleep(1)
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Fusion Skins{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                claim_types = {
                    'OKX_WALLET': {'status': user.get('hasClaimedOkx', False), 'title': 'Connect OKX Wallet'},
                    'BITMART_SIGN_UP': {'status': user.get('hasClaimedBitMart', False), 'title': 'BitMart Sign Up'},
                    'HACKER_LEAGUE': {'status': user.get('hasClaimedHackerLeague', False), 'title': 'Hacker League'}
                }

                for claim_type, details in claim_types.items():
                    completed = False
                    if not details['status']:
                        claim = self.special_tasks(token, claim_type)
                        if claim:
                            bonus = claim.get('items', [])
                            reward = len(bonus) if len(bonus) > 0 else 0
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Special Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {details['title']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward} Skins {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Special Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {details['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)
                    
                    else:
                        completed = True

                if completed:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Special Task{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                tasks = self.tasks(token)
                if tasks:
                    completed = False
                    for task in tasks['tasks']:
                        task_id = task['id']
                        status = task['status']

                        if task and status == 0:
                            start = self.start_tasks(token, task_id)
                            if start:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                                time.sleep(2)

                                claim = self.claim_tasks(token, task_id)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {task['rewardAmount']} $WTON {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(2)

                        elif task and status == 1:
                            claim = self.claim_tasks(token, task_id)
                            if claim:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['rewardAmount']} $WTON {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(2)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

                    progress = self.tasks(token)['taskProgress']
                    if progress >= 3:
                        claim_progress = self.claim_progress_tasks(token)
                        if claim_progress:
                            bonus = claim_progress.get('items', [])
                            reward = len(bonus) if len(bonus) > 0 else 0
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Progress {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward} Skins {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Progress {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} Progress {Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT}Not Eligible to Claim{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )

                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

                skins = self.skins_list(token)
                if skins:
                    have_ton = sum(float(item["value"]) * item["inventory"]  for item in skins if item["sellToken"] == 0)
                    have_usdt = sum(float(item["value"]) * item["inventory"] for item in skins if item["sellToken"] == 1)

                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Info:{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} This Account Have {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}{have_ton:.4f} $TON{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} and {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}{have_usdt:.4f} $USDT{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} From Wonton's Skins {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Skin{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

    def main(self):
        try:
            with open("query.txt", "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            purchase_box = self.question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, purchase_box)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                total_wton, total_ton, total_usdt = self.calculate_balance(queries)
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}[ Account's Total{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {len(queries)} {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}][ Balance's Total{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_wton} $WTON {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_ton:.4f} $TON {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_usdt:.4f} $USDT {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
                )

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Wonton - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = Wonton()
    bot.main()