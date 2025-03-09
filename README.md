# การใช้ Threading ในการดาวน์โหลดข้อมูลจากเว็บไซต์

โปรแกรมนี้แสดงการเปรียบเทียบประสิทธิภาพระหว่างการดาวน์โหลดข้อมูลจากเว็บไซต์แบบลำดับปกติ (Sequential) และแบบใช้ Threading

## หลักการทำงาน

โปรแกรมนี้จะดาวน์โหลดข้อมูลจากเว็บไซต์ Python ที่เกี่ยวข้องหลายเว็บไซต์ โดยเปรียบเทียบเวลาที่ใช้ระหว่างการดาวน์โหลดด้วยสองวิธี:
1. การดาวน์โหลดแบบลำดับปกติ (Sequential)
2. การดาวน์โหลดแบบขนาน (Parallel) โดยใช้ Threading

## ส่วนประกอบหลักของโค้ด

### การนำเข้าโมดูล
```python
import requests
import time
import threading
import concurrent.futures
```
- `requests`: สำหรับการส่ง HTTP requests
- `time`: สำหรับการวัดเวลาการทำงาน
- `threading`: สำหรับการจัดการ threads
- `concurrent.futures`: สำหรับการทำงานแบบขนานอย่างง่าย

### Thread-Local Storage
```python
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session
```

- `thread_local`: เป็นพื้นที่เก็บข้อมูลเฉพาะสำหรับแต่ละ thread
- `get_session()`: สร้างและเก็บ `requests.Session` ไว้เฉพาะสำหรับแต่ละ thread


### ฟังก์ชันการดาวน์โหลด
```python
def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"ดาวน์โหลด {url}: {len(response.content)} ")
```

ฟังก์ชันนี้ดาวน์โหลดข้อมูลจาก URL ที่กำหนดโดยใช้ session ที่เฉพาะสำหรับ thread ปัจจุบัน

### การดาวน์โหลดแบบลำดับปกติ (Sequential)
```python
def download_all_sites_sequential(sites):
    for url in sites:
        download_site(url)
```

วิธีนี้จะดาวน์โหลดแต่ละเว็บไซต์ทีละรายการตามลำดับ ต้องรอให้การดาวน์โหลดก่อนหน้าเสร็จก่อนจึงเริ่มดาวน์โหลดเว็บไซต์ถัดไป

### การดาวน์โหลดโดยใช้ Threading
```python
def download_all_sites_threaded(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)
```

วิธีนี้ใช้ `ThreadPoolExecutor` เพื่อสร้างกลุ่ม threads (pool) ที่มีจำนวนการทำงาน (workers) สูงสุด 5 อัน และกระจายงานดาวน์โหลดเว็บไซต์ไปยัง threads เหล่านี้

## ส่วนหลักของโปรแกรม

```python
if __name__ == "__main__":
    # รายการ URL สำหรับทดสอบ
    sites = [
        "https://www.python.org",
        "https://docs.python.org",
        "https://pypi.org",
    ] * 20  # ทำซ้ำเพื่อให้มีงานมากขึ้น

    # [โค้ดการทดสอบและการวัดเวลา]
```

ส่วนนี้กำหนดรายการ URL ที่จะใช้ทดสอบ และเรียกใช้ทั้งสองวิธีการดาวน์โหลดเพื่อเปรียบเทียบประสิทธิภาพ

## ความแตกต่างระหว่างการดาวน์โหลดแบบปกติและการใช้ Threading

### การดาวน์โหลดแบบปกติ (Sequential)
1. **การทำงานทีละขั้นตอน**: ดาวน์โหลดทีละเว็บไซต์ ต้องรอให้เว็บไซต์ก่อนหน้าดาวน์โหลดเสร็จก่อน
2. **การใช้ทรัพยากร**: ใช้ CPU เพียงหนึ่งคอร์ และมี I/O waiting time สูงเนื่องจากต้องรอการตอบสนองจากเซิร์ฟเวอร์
3. **ความซับซ้อน**: ง่ายต่อการเขียนและเข้าใจ ไม่มีปัญหาเรื่อง race condition
4. **ประสิทธิภาพ**: ไม่เหมาะกับงานที่มี I/O-bound operations จำนวนมาก

### การดาวน์โหลดด้วย Threading
1. **การทำงานแบบขนาน**: ดาวน์โหลดหลายเว็บไซต์พร้อมกัน ทำให้ไม่ต้องรอการตอบสนองจากเว็บไซต์ทีละรายการ
2. **การใช้ทรัพยากร**: ใช้ประโยชน์จาก I/O waiting time โดยสลับไปทำงานอื่นระหว่างรอ
3. **ความซับซ้อน**: ซับซ้อนมากขึ้น ต้องระวังเรื่อง race condition และการแชร์ข้อมูล
4. **ประสิทธิภาพ**: เหมาะอย่างยิ่งกับงานที่มี I/O-bound operations เช่น การดาวน์โหลดจากเว็บไซต์
5. **Thread-Local Storage**: ใช้เพื่อสร้าง session เฉพาะสำหรับแต่ละ thread ช่วยป้องกันปัญหาการแย่งใช้ทรัพยากรร่วมกัน


- Threading เหมาะสำหรับงานที่เป็น I/O-bound (เช่น การดาวน์โหลด การอ่าน/เขียนไฟล์) เพราะ Python จะปล่อย GIL (Global Interpreter Lock (GIL) ซึ่งป้องกันไม่ให้ threads หลาย threads ทำงานพร้อมกันบน CPU หลายคอร์ได้) ระหว่างรอ I/O operations


## สรุป

โค้ดนี้แสดงให้เห็นว่าการใช้ Threading สามารถเพิ่มประสิทธิภาพในการดาวน์โหลดข้อมูลจากเว็บไซต์ได้อย่างมีนัยสำคัญ โดยเฉพาะเมื่อมีการดาวน์โหลดจากหลายเว็บไซต์ ซึ่งเป็นงานประเภท I/O-bound ทั้งนี้ การปรับแต่งจำนวน workers ใน ThreadPoolExecutor ให้เหมาะสมกับงานและทรัพยากรของระบบสามารถช่วยปรับปรุงประสิทธิภาพได้มากยิ่งขึ้น
