import requests
import time
import threading
import concurrent.futures

# สร้าง thread-local storage สำหรับเก็บ session
thread_local = threading.local()


def get_session():
    # สร้าง session เฉพาะสำหรับแต่ละ thread
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    # ดึงข้อมูลจาก URL โดยใช้ session ที่เฉพาะสำหรับ thread นี้
    session = get_session()
    with session.get(url) as response:
        print(f"ดาวน์โหลด {url}: {len(response.content)} ")


def download_all_sites_sequential(sites):
    # ดาวน์โหลดแบบลำดับปกติ
    for url in sites:
        download_site(url)


def download_all_sites_threaded(sites):
    # ดาวน์โหลดแบบใช้ Threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    # รายการ URL สำหรับทดสอบ
    sites = [
        "https://www.python.org",
        "https://docs.python.org",
        "https://pypi.org",
    ] * 20  # ทำซ้ำเพื่อให้มีงานมากขึ้น

    # ทดสอบแบบลำดับปกติ
    print("เริ่มดาวน์โหลดแบบลำดับปกติ...")
    start_time = time.time()
    download_all_sites_sequential(sites)
    sequential_time = time.time() - start_time
    print(f"จบการดาวน์โหลดแบบลำดับปกติ")

    # ทดสอบแบบ Threading
    print("\nเริ่มดาวน์โหลดแบบ Threading...")
    start_time = time.time()
    download_all_sites_threaded(sites)
    threaded_time = time.time() - start_time
    print(f"จบการดาวน์โหลดแบบ Threading")

    print(f"เวลาที่ใช้แบบลำดับปกติ: {sequential_time:.2f} วินาที")
    print(f"เวลาที่ใช้แบบ Threading: {threaded_time:.2f} วินาที")

    # เปรียบเทียบผล
    improvement = (sequential_time - threaded_time) / sequential_time * 100
    print(f"\nการใช้ Threading ช่วยลดเวลาได้: {improvement:.2f}%")
