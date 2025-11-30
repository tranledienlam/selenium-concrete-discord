
import argparse
from selenium_browserkit import BrowserManager, Node, By, Utility


PROJECT_URL = "https://discord.com"

class Setup:
    def __init__(self, node: Node, profile) -> None:
        self.node = node
        self.profile = profile
        
        self.run()

    def run(self):
        self.node.new_tab(f'{PROJECT_URL}', method="get")
        Utility.wait_time(10)

class Auto:
    def __init__(self, node: Node, profile: dict) -> None:
        self.driver = node._driver
        self.node = node
        self.profile_name = profile.get('profile_name')
        self.email = profile.get('email')
        self.pwd_discord = profile.get('pwd_discord')

    def wait_delay(self):
        text_countdown = self.node.get_text(By.CSS_SELECTOR, '[class*="cooldown"]', timeout=10)
        if text_countdown:
            if ':' in text_countdown:
                seconds = 0
                parts = text_countdown.split(':')
                if len(parts) == 2:
                    seconds = int(parts[-2]) * 60 + int(parts[-1])
                elif len(parts) == 3:
                    seconds = int(parts[-3]) * 3600 + int(parts[-2]) * 60 + int(parts[-1])

                if seconds and seconds.is_integer():
                    return self.node.wait_for_disappear(By.XPATH, '//*[contains(@class, "cooldown")][contains(text(), ":")]', timeout=int(seconds))
                else:
                    self.node.log('Không thể lấy số giây delay')
                
            else:
                return True
        else:
            self.node.log('Không tìm thấy class cooldown')
    
    def answer_ai(self):
        return self.node.ask_ai(f'Trả lời ngắn gọn bằng tiếng anh (không cần giải thích, không có xuống dòng), tối đa 10 từ. Nội dung trả lời liên quan tới các tin nhắn gần nhất theo tấm ảnh cung cấp. Ưu tiên lời chào hỏi')
    
    def send_message(self, text):
        if self.node.find(By.CSS_SELECTOR, '[role="textbox"]'):
            self.wait_delay()
            answer = self.answer_ai()
            if answer:
                text = answer
            if self.node.find_and_input(By.CSS_SELECTOR, '[role="textbox"]', text):
                self.node.press_key('enter')
                self.node.press_key('enter')
                return text
        else:
            self.node.log('Không tìm thấy input message')
            return False
    
    def check_login(self):
        btn_login = self.node.get_text(By.ID, 'login')
        if btn_login:
            if btn_login.lower() == "Open Discord".lower():
                self.node.log('Đã login discord')
                return True
            elif btn_login.lower() == "Log In".lower():
                self.node.log('Chưa login discord')
                return False
        self.node.log('Không xác định được login discord hay chưa')
        return None
    
    def login(self):
        is_login = self.check_login()
        if is_login == True:
            return True
        elif is_login == False:
            if not (self.email and self.pwd_discord):
                self.node.log(f'Không có email và mật khẩu discord để đăng nhập')
                return False
    
            self.node.go_to(f'{PROJECT_URL}/login')
            if self.node.has_texts('Choose an account'):
                self.node.find_and_click(By.XPATH, '//span[contains(text(),"Log in")]')
            self.node.find_and_input(By.CSS_SELECTOR, '[name="email"]', self.email, delay=0.2)
            self.node.find_and_input(By.CSS_SELECTOR, '[name="password"]', self.pwd_discord, delay=0.2)
            self.node.press_key('Enter')

            self.node.go_to(PROJECT_URL)
            return self.check_login()
        elif is_login == None:
            return None
    def run(self):
        self.node.go_to(f'{PROJECT_URL}', method="get")
        return self.login()

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