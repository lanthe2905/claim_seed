# import webbrowser
# url = 'https://web.telegram.org/a/#-6508172553'

# # webbrowser.get(chrome_path).open(url)
# webbrowser.open_new_tab(url)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run():
  # Tạo đối tượng Options cho Chrome
  chrome_options = Options()
  profile_path = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Person1"
  chrome_options.add_argument(f"user-data-dir={profile_path}")  # Thêm dòng này để sử dụng hồ sơ người dùng hiện tại

  service = Service(ChromeDriverManager().install())

  driver = webdriver.Chrome(service=service, options=chrome_options)
  # Mở URL
  url = 'https://web.telegram.org/a/#-6508172553'
  driver.get(url)
  # Đợi cho đến khi trang được tải xong, có thể thêm các điều kiện chờ cụ thể ở đây

  import time 
  time.sleep(2) # Đợi 5 giây để chờ trang tải xong

  sidebar_seed_forum = driver.find_element(by= By.XPATH, value='//a[@href="#6508172553"]')
  sidebar_seed_forum.click()
  time.sleep(3)

  play_button = driver.find_element(by= By.CLASS_NAME, value='bot-menu-text')
  play_button.click()
  time.sleep(1)

  i_frame = driver.find_element(by= By.TAG_NAME, value='iframe')
  str_src = i_frame.get_attribute('src')
  #Lưu src vào file query txt
  with open('query.txt', 'w') as f:
    import re
    from urllib.parse import unquote
    # decode_src = unquote(str_src) #decode mã URL
    matches = re.search(r'tgWebAppData=([^&]*)', str_src)
    decode_src = unquote(str(matches.group(1))) #decode mã URL

    f.write(str(decode_src))


  # Lấy mã HTML của trang
  # Đóng trình duyệt
  # driver.quit()