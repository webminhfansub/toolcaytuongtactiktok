import time

import threading

import os

from datetime import datetime, timezone

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.common.alert import Alert

from undetected_chromedriver import Chrome

from pystyle import Colors, Colorate, Write, Center

import re





def get_current_time():

    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")



class ZefoyBot:

    def __init__(self, headless=True):

        self.start_time = get_current_time()

        self.session_stats = {

            "success_count": 0,

            "total_views": 0,

            "errors": 0

        }

        self.services = {

            "1": {

                "name": "Followers", 

                "button": "t-followers-button", 

                "enabled": False,

                "increment": 0,

                "info": "Chưa khả dụng"

            },

            "2": {

                "name": "Hearts", 

                "button": "t-hearts-button", 

                "enabled": True,

                "increment": 30,

                "info": "Mỗi lần +30 tim"

            },

            "3": {

                "name": "Comments Hearts", 

                "button": "t-chearts-button", 

                "enabled": True,

                "increment": 10,

                "info": "Mỗi lần +10 tim comment"

            },

            "4": {

                "name": "Views", 

                "button": "t-views-button", 

                "enabled": True,

                "increment": 500,

                "info": "Mỗi lần +500 views"

            },

            "5": {

                "name": "Shares", 

                "button": "t-shares-button", 

                "enabled": True,

                "increment": 150,

                "info": "Mỗi lần +150 shares"

            },

            "6": {

                "name": "Favorites", 

                "button": "t-favorites-button", 

                "enabled": True,

                "increment": 90,

                "info": "Mỗi lần +90 favorites"

            },

            "7": {

                "name": "Live Stream", 

                "button": "t-livestream-button", 

                "enabled": False,

                "increment": 0,

                "info": "Chưa khả dụng"

            }

        }

        self.current_service = None  # Thêm biến để lưu service hiện tại

        chrome_options = Options()

        if headless:

            chrome_options.add_argument("--headless=new")

            chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument("--window-size=1920,1080")

        chrome_options.add_argument("--log-level=3")

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = Chrome(options=chrome_options)

        self.wait = WebDriverWait(self.driver, 15)

        self.headless = headless

    def print_services_menu(self):

        menu_box = """

╔═══════════════════ DỊCH VỤ ══════════════════╗

"""

        for key, service in self.services.items():

            status = "✅" if service["enabled"] else "❌"

            menu_box += f"║ {key}. {service['name']} {status}\n"

            menu_box += f"║    💫 {service['info']}{' ' * (40 - len(service['info']))}║\n"

        menu_box += "╚═══════════════════════════════════════════╝"

        print(Colorate.Horizontal(Colors.blue_to_purple, menu_box))

# check dịch vụ không hoạt động

    def select_service(self):

        while True:

            self.print_services_menu()

            choice = Write.Input("🔧 Chọn dịch vụ (1-7): ", Colors.cyan, interval=0.01)

            

            if choice in self.services:

                service = self.services[choice]

                if service["enabled"]:

                    try:

                        button = self.wait.until(

                            EC.element_to_be_clickable(

                                (By.CLASS_NAME, service["button"])

                            )

                        )

                        button.click()

                        self.current_service = service  # Lưu service đã chọn

                        success_box = f"""

╔════════════ CHỌN DỊCH VỤ ════════════╗

║ ✅ Đã chọn: {service['name']}{' ' * (25 - len(service['name']))}║

║ 💫 {service['info']}{' ' * (35 - len(service['info']))}║

╚═══════════════════════════════════════╝

"""

                        print(Colorate.Horizontal(Colors.green_to_blue, success_box))

                        return True

                    except Exception as e:

                        error_box = f"""

╔════════════ LỖI ════════════╗

║ ❌ Không thể chọn dịch vụ    ║

║ 🔄 Vui lòng thử lại         ║

╚═══════════════════════════════╝

"""

                        print(Colorate.Horizontal(Colors.red_to_yellow, error_box))

                else:

                    print(Colorate.Horizontal(Colors.red_to_yellow, "❌ Dịch vụ này hiện không khả dụng!"))

            else:

                print(Colorate.Horizontal(Colors.red_to_yellow, "❌ Lựa chọn không hợp lệ!"))





    def print_success(self):

        if self.current_service:

            increment = self.current_service["increment"]

            service_name = self.current_service["name"]

            self.session_stats["success_count"] += 1

            self.session_stats["total_views"] += increment

            

            success_box = f"""

╔════════════════ THÀNH CÔNG ═══════════════╗

║ ✨ Lượt buff thứ: {self.session_stats['success_count']}{' ' * (20 - len(str(self.session_stats['success_count'])))}║

║ 🔥 +{increment} {service_name}{' ' * (30 - len(str(increment)) - len(service_name))}║

║ 📊 Tổng: {self.session_stats['total_views']} {service_name}{' ' * (25 - len(str(self.session_stats['total_views'])) - len(service_name))}║

╚════════════════════════════════════════════╝

            """

            print(Colorate.Diagonal(Colors.green_to_blue, Center.XCenter(success_box)))



    def handle_alert(self):

        try:

            WebDriverWait(self.driver, 2).until(EC.alert_is_present())

            Alert(self.driver).dismiss()

        except:

            pass



    def wait_for_ad_to_finish(self):

        try:

            # Chờ trang load 30s đầu tiên

            print("Đang chờ trang tải hoàn tất...")

            for i in range(30,0,-1):

                print(f"\rĐang chờ {i}s để trang load...", end="")

                time.sleep(1)

            print("\nĐã chờ xong 30s đầu!")

    

            try:

                # Phát hiện và click nút xem quảng cáo

                ad_container = self.driver.find_element(By.CLASS_NAME, "fc-monetization-dialog-container")

                

                if ad_container:

                    print("Đã tìm thấy quảng cáo!")

                    ad_button = ad_container.find_element(By.CLASS_NAME, "fc-rewarded-ad-button") 

                    

                    if ad_button:

                        print("Đang click nút xem quảng cáo...")

                        ad_button.click()

                        

                        # Chờ 30s xem quảng cáo

                        print("\nPhát hiện quảng cáo...")

                        for i in range(10,0,-1):

                            print(f"\rĐang lách quảng cáo: chờ {i}s", end="")

                            time.sleep(1)                        

                        # Refresh trang và chờ thêm 15s

                        print("Đã lách xong...")

                        self.driver.refresh()

                        time.sleep(15)

                        print("Bú luôn!")

                        return True

                        

            except Exception as e:

                print(f"Không tìm thấy quảng cáo: {str(e)}")

                return False

    

        except Exception as e:

            print(f"Lỗi: {str(e)}")

            return False



    def solve_captcha_manually(self):

        try:

            self.handle_alert()

            captcha = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/form/div/div/img")))

            captcha.screenshot("captcha.png")

            

            captcha_box = f"""

╔═══════════════ CAPTCHA ═══════════════╗

║ 📸 Đã lưu ảnh captcha: captcha.png    ║

╚═══════════════════════════════════════╝

            """

            print(Colorate.Horizontal(Colors.blue_to_purple,captcha_box))

            

            answer = Write.Input("🔑 Nhập mã captcha: ", Colors.cyan, interval=0.01)

            

            self.driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/form/div/div/div/input").send_keys(answer)

            self.driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/form/div/div/div/div/button").click()

            time.sleep(5)

            self.driver.refresh()

            time.sleep(3)

            

        except TimeoutException:

            self.session_stats["errors"] += 1

            self.driver.quit()

            exit()



    def submit_video_link(self, video_url):

        try:

            visible_forms = self.driver.find_elements(By.XPATH, "//form[not(contains(@class, 'nonec'))]")

            for form in visible_forms:

                try:

                    link_input = form.find_element(By.XPATH, ".//input[contains(@placeholder, 'Enter')]")

                    search_btn = form.find_element(By.XPATH, ".//button[contains(., 'Search')]")

                    link_input.clear()

                    link_input.send_keys(video_url)

                    search_btn.click()

                    time.sleep(2)

                    return True

                except:

                    continue

            return False

        except Exception as e:

            self.session_stats["errors"] += 1

            return False



    def wait_for_timer_or_confirm(self):

        try:

            while True:

                self.handle_alert()

                try:

                    timer_element = self.driver.find_element(By.XPATH, "//div[contains(text(),'Please wait') or contains(text(),'Wait')]")

                    timer_text = timer_element.text

                    waiting_box = f"""

╔═══════════════ ĐANG CHỜ ═══════════════╗

║ ⏳ {timer_text}                         ║

║ 📊 Views hiện tại: {self.session_stats['total_views']}            ║

╚═══════════════════════════════════════════╝

                    """

                    print(Colorate.Horizontal(Colors.yellow_to_red, Center.XCenter(waiting_box)))

                    time.sleep(5)

                except NoSuchElementException:

                    break



            try:

                wbutton = self.driver.find_element(By.XPATH, "//button[contains(@class, 'wbutton')]")

                wbutton.click()

                self.session_stats["success_count"] += 1

                return True

            except NoSuchElementException:

                pass



            buttons = self.driver.find_elements(By.XPATH, "//button[not(contains(@class, 'disableButton'))]")

            for btn in buttons:

                text = btn.text.strip().lower()

                if any(x in text for x in ["send", "again", "views", "hearts", "shares", "favorites"]):

                    btn.click()

                    self.session_stats["success_count"] += 1

                    return True

                if re.match(r"\d+\s*(views|hearts|shares|favorites)?", text):

                    btn.click()

                    self.session_stats["success_count"] += 1

                    return True



            return False



        except Exception as e:

            self.session_stats["errors"] += 1

            return False



    def run(self, video_url):

        try:

            self.driver.quit()

        except:

            pass

        

        try:

            self.__init__(headless=False)

            self.driver.get("https://zefoy.com")

            self.handle_alert()

            self.wait_for_ad_to_finish()

            self.solve_captcha_manually()

            self.handle_alert()



            # Thay thế phần chọn dịch vụ thủ công bằng hàm tự động

            if not self.select_service():

                return



            while True:

                if "502" in self.driver.page_source:

                    time.sleep(60)

                    self.driver.get("https://zefoy.com")

                    continue

                

                try:

                    if self.submit_video_link(video_url):

                        if self.wait_for_timer_or_confirm():

                            self.print_success()

                            time.sleep(30)

                        else:

                            time.sleep(5)

                except Exception as e:

                    self.session_stats["errors"] += 1

                    time.sleep(30)

                    

        except Exception as e:

            self.session_stats["errors"] += 1



def print_banner():

    banner = f"""

╔══════════════════════════════════════════════════════════════╗

║          ZEFOY BOT MINHFANSUB BẢN LÁCH QUẢNG CÁO V2.0        ║

╟──────────────────────────────────────────────────────────────╢

║  ⭐ Tăng View, Tim, Follows TikTok Tự Động                  ║

║  ⏰ {get_current_time()}                                    ║

║  👤 User: {os.getenv('USER', 'MINHFANSUBDEV')}                 ║

╚══════════════════════════════════════════════════════════════╝    

    """

    print(Colorate.Diagonal(Colors.red_to_blue, banner))



if __name__ == '__main__':

    print_banner()

    link = Write.Input("🔗 Nhập link video TikTok: ", Colors.cyan, interval=0.01)

    bot = ZefoyBot()

    thread = threading.Thread(target=bot.run, args=(link,))

    thread.start()

    

    start_box = f"""

╔═══════════════ KHỞI CHẠY ═══════════════╗

║ ✨ Bot đang chạy ...                   ║

║ 📱 Bạn có thể thu nhỏ cửa sổ này        ║

╚════════════════════════════════════════════╝

    """



    print(Colorate.Horizontal(Colors.green_to_blue, start_box))

