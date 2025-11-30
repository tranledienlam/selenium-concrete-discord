
import argparse
from random import choice
from selenium_browserkit import BrowserManager, Node, By, Utility
from discord import Setup as DiscordSetup, Auto as DiscordAuto

PROJECT_URL = "https://discord.com/channels/1220537696087445565/1222214709265305634"

MESSAGES = [
    "Hello everyone! Anyone online? 😊",
    "Hey guys, hope you're all having a great day!",
    "Hi team! What are you all up to? 😄",
    "Hey everyone, I just joined in!",
    "Hello folks, any updates today?",
    "Hi all, I'm new to the server!",
    "Hey everyone, looking forward to chatting with you!",
    "Hi guys, hope you're doing well!",
    "Good morning everyone! ☀️",
    "Good evening guys! 🌙",
    "Hello hello, anyone free to chat? 😆",
    "Hey team, hope your day is going smoothly!",
    "Hi everyone, I'm here! 👋",
    "Hey guys, I'm back online!",
    "What's up team, any new drama today? 🤣",
    "Hey everyone, I need a little help!",
    "Hope you're all having a fantastic day!",
    "Heyyyyy, long time no see!",
    "Hi all, nice to meet you!",
    "Hello server! Wishing everyone a great day!"
]

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        
        self.run()

    def run(self):
        DiscordSetup(node=self.node, profile=self.profile)
        Utility.wait_time(10)

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node

        self.discord_auto = DiscordAuto(node=node, profile=profile)
        self.run()
    
    def run(self):
        sended = 0
        if not self.discord_auto.run():
            self.node.snapshot('Chưa login discord')
            return 
        self.node.go_to(f'{PROJECT_URL}', method="get")
        
        times = 1   # số lần gửi
        delay = 600 # thời gian chờ gửi tin kế tiếp (giây)
        
        for i in range(times):
            message = self.discord_auto.send_message(choice(MESSAGES))
            if message:
                sended += 1
                if i == times -1:
                    break
                Utility.wait_time(delay)
            else:
                break
        self.node.snapshot(f'Số lượng tin nhắn đã gửi: {sended}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help="Chạy ở chế độ tự động")
    parser.add_argument('--headless', action='store_true', help="Chạy trình duyệt ẩn")
    parser.add_argument('--disable-gpu', action='store_true', help="Tắt GPU")
    args = parser.parse_args()

    profiles = Utility.read_data('profile_name', 'email', 'pwd_discord')
    max_profiles = Utility.read_config('MAX_PROFLIES')

    if not profiles:
        print("Không có dữ liệu để chạy")
        exit()

    browser_manager = BrowserManager(auto_handler=Auto, setup_handler=Setup)
    browser_manager.update_config(
                        headless=args.headless,
                        disable_gpu=args.disable_gpu,
                        use_tele=True,
                        use_ai=True
                    )
    # browser_manager.add_extensions('Meta-Wallet-*.crx','OKX-Wallet-*.crx')
    browser_manager.run_menu(
        profiles=profiles,
        max_concurrent_profiles=max_profiles,
        auto=args.auto
    )