import time
import random
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# Lấy GitHub username tự động
github_user = os.getenv("GITHUB_ACTOR", "vonga2221983")
URL = f"https://adnade.net/ptp/?user=tuanzobe&subid={github_user}"
print("URL đang mở:", URL)

TOTAL_RUN_HOURS = 6   # mỗi job tối đa 6 giờ
OPEN_MINUTES = 60      # mở trang 60 phút
DELAY_MINUTES = 3      # nghỉ 3–5 phút giữa các vòng

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17 Safari/605.1.15"
]

def human_actions(page):
    """Fake hành vi người dùng"""
    for _ in range(random.randint(3, 7)):
        x = random.randint(100, 1500)
        y = random.randint(100, 900)
        page.mouse.move(x, y, steps=random.randint(10, 30))
        if random.random() < 0.2:
            page.mouse.click(x, y)
        time.sleep(random.uniform(0.5, 2.0))
    for _ in range(random.randint(1, 3)):
        page.mouse.wheel(0, random.randint(200, 600))
        time.sleep(random.uniform(0.5, 1.5))

def disable_automation(page):
    """Ẩn Playwright"""
    page.evaluate("""
        () => {
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            delete navigator.__proto__.webdriver;
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        }
    """)

def run_loop():
    end_time = time.time() + TOTAL_RUN_HOURS * 3600
    counter = 0

    with sync_playwright() as p:
        while time.time() < end_time:
            counter += 1
            ua = random.choice(USER_AGENTS)
            print(f"\n[{datetime.now()}] LOOP #{counter} - User-Agent: {ua}")

            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-gpu"]
            )
            page = browser.new_page(
                user_agent=ua,
                viewport={"width": random.randint(1100, 1920), "height": random.randint(800, 1080)},
                timezone_id="Asia/Ho_Chi_Minh",
                locale="en-US"
            )

            disable_automation(page)
            print(f"👉 Mở trang: {URL}")
            page.goto(URL, wait_until="load")
            print(f"⏳ Giữ trang mở ~{OPEN_MINUTES} phút...")
            human_actions(page)
            time.sleep(OPEN_MINUTES * 60)

            browser.close()
            rest = random.randint(DELAY_MINUTES, DELAY_MINUTES + 2)
            print(f"⏲ Nghỉ {rest} phút trước vòng tiếp theo...")
            time.sleep(rest * 60)

    print("✅ Hoàn tất 6 giờ chạy — Workflow sẽ tự chạy lại nếu không có job cũ đang chạy.")

if __name__ == "__main__":
    run_loop()
