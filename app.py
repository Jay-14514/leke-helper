from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSelectorException
from selenium.webdriver.chrome.options import Options
import time
import signal
import re
from datetime import datetime  # 新增：标准日志时间戳

# 全局变量：标记是否继续监听
continue_monitor = True

def get_log_time():
    """生成标准日志时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def signal_handler(sig, frame):
    """捕获Ctrl+C终止监听"""
    global continue_monitor
    print(f"\n[{get_log_time()}] 终止：终止指令已触发，正在停止监听...")
    continue_monitor = False

signal.signal(signal.SIGINT, signal_handler)

def calculate_add_sub(question_text):
    # 清洗题目文本（去除空格、问号、等号等干扰）
    clean_text = question_text.strip().replace(" ", "").replace("？", "").replace("=", "").replace("?", "")
    print(f"\n[{get_log_time()}] 信息：识别题目：{question_text}")
    print(f"[{get_log_time()}] 信息：清洗后：{clean_text}")
    
    # 匹配加法（+ / ＋）
    add_pattern = r"(\d+)(\+|＋)(\d+)"
    add_match = re.search(add_pattern, clean_text)
    if add_match:
        num1 = int(add_match.group(1))
        num2 = int(add_match.group(3))
        result = num1 + num2
        print(f"[{get_log_time()}] 信息：加法计算：{num1} + {num2} = {result}")
        return str(result)
    
    # 匹配减法（- / －）
    sub_pattern = r"(\d+)(-|－)(\d+)"
    sub_match = re.search(sub_pattern, clean_text)
    if sub_match:
        num1 = int(sub_match.group(1))
        num2 = int(sub_match.group(3))
        result = num1 - num2
        print(f"[{get_log_time()}] 信息：减法计算：{num1} - {num2} = {result}")
        return str(result)
    
    print(f"[{get_log_time()}] 警告：未识别到加减法题目")
    return ""

def find_and_answer_roll_call(driver):
    try:
        # 1. 精准定位点名答题弹窗（ant-modal-content类，乐课网核心弹窗）
        popup_elem = driver.find_element(
            By.XPATH, '//div[@class="ant-modal-content" and .//span[@class="rollCall-student-header"]]'
        )
        if not popup_elem.is_displayed():
            return False
        
        # 2. 提取题目文本（精准匹配question类）
        question_elem = popup_elem.find_element(By.XPATH, './/span[@class="question"]')
        question_text = question_elem.text.strip()
        if not question_text:
            print(f"[{get_log_time()}] 警告：未提取到题目文本")
            return False
        
        # 3. 计算加减法答案
        answer = calculate_add_sub(question_text)
        if not answer:
            return False
        
        # 4. 精准定位answer选项并点击（匹配答案文本）
        answer_elems = popup_elem.find_elements(By.XPATH, './/span[@class="answer"]')
        for elem in answer_elems:
            elem_text = elem.text.strip()
            if elem_text == answer:
                print(f"[{get_log_time()}] 信息：匹配到正确答案选项：{elem_text}，点击选择")
                # 适配antd组件的点击（避免点击失效）
                driver.execute_script("arguments[0].click();", elem)
                time.sleep(0.5)
                
                # 5. 兜底：检查是否有提交按钮（若需要）
                try:
                    submit_elem = popup_elem.find_element(
                        By.XPATH, './/button[contains(text(), "提交") or contains(text(), "确认")]'
                    )
                    if submit_elem.is_enabled():
                        print(f"[{get_log_time()}] 信息：点击提交按钮")
                        driver.execute_script("arguments[0].click();", submit_elem)
                except NoSuchElementException:
                    print(f"[{get_log_time()}] 信息：无提交按钮，选择答案即完成答题")
                
                return True
        
        print(f"[{get_log_time()}] 警告：未找到答案为「{answer}」的选项，选项列表：{[e.text.strip() for e in answer_elems]}")
        return False
    
    except NoSuchElementException:
        # 兜底：兼容单纯点名按钮场景
        try:
            roll_call_btn = driver.find_element(
                By.XPATH, '//*[contains(text(), "点名") and (self::button or self::div)]'
            )
            if roll_call_btn.is_displayed():
                print(f"[{get_log_time()}] 信息：匹配到单纯点名按钮，点击完成")
                driver.execute_script("arguments[0].click();", roll_call_btn)
                return True
        except:
            pass
        return False
    except Exception as e:
        print(f"[{get_log_time()}] 错误：答题流程异常：{str(e)}")
        return False

def leke_live_roll_call():
    # 1. 配置Chrome选项（连接调试窗口）
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-popup-blocking")
    
    driver = None
    try:
        # 2. 连接Chrome
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(3)  # 适配antd组件加载
        print(f"[{get_log_time()}] 信息：已连接Chrome | 乐课网ant-modal弹窗监控启动")
        
        # 3. 持续监听主循环
        global continue_monitor
        while continue_monitor:
            current_url = driver.current_url
            print(f"\n[{get_log_time()}] 信息：监控中 | 页面：{current_url} | 时间：{time.strftime('%H:%M:%S')}")
            
            # 域名校验
            if "leke.cn" not in current_url:
                print(f"[{get_log_time()}] 错误：非乐课网页面，2秒后重试...")
                time.sleep(2)
                continue
            
            # 直播页校验
            if "student" not in current_url and "interact-classroom" not in current_url:
                print(f"[{get_log_time()}] 警告：非学生端直播页，等待切换...")
                time.sleep(2)
                continue
            
            # 4. 8秒窗口期检测（精准匹配ant-modal弹窗）
            start_time = time.time()
            answered = False
            while time.time() - start_time < 8 and continue_monitor:
                if find_and_answer_roll_call(driver):
                    answered = True
                    print(f"[{get_log_time()}] 信息：本轮点名答题完成！")
                    break
                time.sleep(0.2)  # 高频轮询（0.2秒），适配倒计时弹窗
            
            if not answered and continue_monitor:
                print(f"[{get_log_time()}] 信息：本轮8秒未检测到点名答题弹窗，继续监听...")
            
            time.sleep(0.5)  # 降低CPU占用
    
    except Exception as e:
        print(f"\n[{get_log_time()}] 错误：监控核心异常：{str(e)}")
        print(f"[{get_log_time()}] 提示：浏览器窗口保留，可手动操作")
    finally:
        if driver:
            driver.quit()
            print(f"[{get_log_time()}] 信息：driver连接已释放，Chrome窗口正常使用")

if __name__ == "__main__":
    leke_live_roll_call()