from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By  # 添加此行以导入 By 类
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_answer(driver,q):
    driver.execute_script("window.open('https://chat.baidu.com/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])  # 切换到新标签页
    enter_box = driver.find_element(By.ID, "chat-input-box")
    sleep(2)
    enter_box.send_keys(q)
    sleep(2)

    button = driver.find_element(By.CLASS_NAME, "cs-input-model")
    button.click()

    elements = driver.find_elements(By.CLASS_NAME, 'input-capsules-model-list-item')
    button = elements[0]  # 索引从0开始
    button.click()

    enter_box.send_keys(Keys.ENTER)
    sleep(2)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'p.marklang-paragraph'))
    )
    text = element.text
    print(text)
    return text
def login_a3000(driver):
    enter_box = driver.find_element(By.ID, "login_name1")
    enter_box.send_keys("在这里修改账户")

    enter_box = driver.find_element(By.ID, "password1")
    enter_box.send_keys("在这里修改密码")

    button = driver.find_element(By.ID, "loginButton")
    button.click()

    button1 = driver.find_element(By.NAME, "at_home")
    button1.click()

    button1 = driver.find_element(By.NAME, "go")
    button1.click()

def unreal_test(driver):

    button1 = driver.find_element(By.ID, "btn_next")
    button1.click()

    for i in range(40):
        container = driver.find_element(By.CLASS_NAME, "question-container")

        # 获取所有<p>标签文本（过滤空文本）
        paragraphs = [p.text for p in container.find_elements(By.TAG_NAME, "p") if p.text.strip()]

        # 提取阅读内容（第二个非空<p>）
        reading_content = paragraphs[1] if len(paragraphs) > 1 else ""
        # 提取问题（第四个非空<p>）
        question = paragraphs[3] if len(paragraphs) > 3 else ""

        print(f"阅读内容: {reading_content}")
        print(f"问题: {question}")
        sleep(0.5)
        options = driver.find_elements(By.CSS_SELECTOR, ".activity-option .mc-option")
        option_texts = [opt.text for opt in options]

        print("选项文字:", option_texts)  # 输出: ['catch', 'fly', 'buy', 'help']
        test = get_answer(driver,f"阅读内容: {reading_content}"+"\n"+f"问题: {question}"+"\n"+"选项文字:"+str(option_texts)+"\n"+"只回答我一个代表选项（第一个选项是A，第二个是B，以此类推）大写英文字母，其他什么都不要回答")
        sleep(10)
        driver.switch_to.window(driver.window_handles[0])
        sleep(0.5)
        element = driver.find_element(By.XPATH, f"//span[text()='{test}']/..")
        driver.execute_script("arguments[0].click();", element)

        button1 = driver.find_element(By.XPATH, '//button[@class="submit-button submit fcs-fixed ng-binding ng-scope"]')
        button1.click()
    # option.click()
# 配置驱动路径（替换为你的实际路径）

def zuoti(driver):
    # driver.execute_script("arguments[0].click();",
    #                       driver.find_element(By.CSS_SELECTOR, '.MuiButton-contained'))
    # start_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Start Lesson"]'))
    # )
    # start_button.click()
    sleep(15)
    for i in range(10):
        te = driver.find_element(By.ID, "question-text")
        print(te.text)

        radio_group = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[role="radiogroup"]'))
        )

        # 获取所有单选按钮
        radio_buttons = radio_group.find_elements(By.CSS_SELECTOR, '[role="radio"]')
        buttons = []
        # 依次点击每个按钮
        for button in radio_buttons:
            button.click()
            buttons.append(button.text)
            print(f"已点击: {button.text}")


        container = driver.find_element(By.ID, "start-reading")
        paragraphs = [p.text for p in container.find_elements(By.TAG_NAME, "p") if p.text.strip()]
        text = get_answer(driver,str(paragraphs)+str(buttons)+"只回答我一个代表选项（第一个选项是A，第二个是B，以此类推）大写英文字母，其他什么都不要回答")
        sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        r1 = {"A":0,"B":1,"C":2,"D":3}
        radio_buttons[r1[text]].click()
        sleep(1)
        # 复合选择器定位按钮
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.MuiButton-containedPrimary"))
        )
        button.click()
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.MuiButton-containedPrimary"))
        )
        button.click()
        sleep(20)
        print(paragraphs)
edge_driver_path = r"msedgedriver.exe"  # :ml-citation{ref="1,8" data="citationList"}

service = Service(edge_driver_path)
driver = webdriver.Edge(service=service)
driver.implicitly_wait(2)
driver.get("https://portal.achieve3000.net/index")
# get_answer(driver)
# sleep(10)
# quit()
login_a3000(driver)
current_url = driver.current_url
if current_url == "https://portal.achieve3000.net/kb/levelset/welcome":
    unreal_test(driver)
else:
    zuoti(driver)
sleep(100)
# 关闭浏r览器
driver.quit()
