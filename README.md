# AFT.SBTVC_BOT

Discord Bot สำหรับช่วยจัดการเซิร์ฟเวอร์ **AFT.SBTVC** ของ อวท.

## ระบบที่มีแล้ว

### ทั่วไป
- `/ทดสอบ` ตรวจสอบสถานะบอทและ Ping
- `/ช่วยเหลือ` ดูรายการคำสั่งทั้งหมด

### ประกาศ
- `/ประกาศ` สร้างประกาศแบบ Embed
- จำกัดผู้ใช้คำสั่งไว้ที่ผู้มีสิทธิ์ **Manage Messages**

### การประชุม
- `/ประชุม สร้าง` สร้างประกาศนัดประชุม
- `/ประชุม ล่าสุด` ดูการประชุมล่าสุด

### เช็กชื่อ
- `/เช็กชื่อ เปิด` เปิดรอบเช็กชื่อ
- `/เช็กชื่อ ลงชื่อ` สมาชิกลงชื่อเข้าร่วม
- `/เช็กชื่อ รายชื่อ` ดูรายชื่อผู้เข้าร่วม
- `/เช็กชื่อ ปิด` ปิดรอบเช็กชื่อ

### ติดตามงาน
- `/งาน เพิ่ม` สร้างงานและมอบหมายผู้รับผิดชอบ
- `/งาน รายการ` ดูงานที่กำลังดำเนินการ
- `/งาน เสร็จ` ปิดงานเป็นเสร็จสิ้น

## โครงสร้างโปรเจกต์

```text
AFT.SBTVC_BOT/
├── main.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── README.md
└── cogs/
    ├── __init__.py
    ├── general.py
    ├── announcements.py
    ├── meetings.py
    ├── attendance.py
    └── tasks.py
```

ฐานข้อมูลใช้ **SQLite** และจะสร้างไฟล์ `aft_sbtvc.db` อัตโนมัติเมื่อบอทเริ่มทำงานครั้งแรก

## 1. ติดตั้ง Python

แนะนำ Python 3.11 หรือใหม่กว่า

ตรวจสอบเวอร์ชัน:

```bash
python --version
```

## 2. Clone Repository

```bash
git clone https://github.com/SBTVC/AFT.SBTVC_BOT.git
cd AFT.SBTVC_BOT
```

## 3. สร้าง Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

ติดตั้งแพ็กเกจ:

```powershell
pip install -r requirements.txt
```

## 4. ตั้งค่า Environment Variables

คัดลอก `.env.example` เป็น `.env`

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

จากนั้นแก้ `.env`

```env
DISCORD_TOKEN=ใส่_BOT_TOKEN_ตรงนี้
DISCORD_GUILD_ID=ใส่_SERVER_ID_AFT_SBTVC_ตรงนี้
```

### วิธีหา Server ID

1. Discord → User Settings → Advanced
2. เปิด **Developer Mode**
3. คลิกขวาที่เซิร์ฟเวอร์ AFT-SBTVC
4. เลือก **Copy Server ID**

> ห้ามใส่ Token จริงลงในไฟล์ที่ Commit ขึ้น GitHub  
> ไฟล์ `.env` ถูกเพิ่มไว้ใน `.gitignore` แล้ว

## 5. รันบอท

```powershell
python main.py
```

เมื่อสำเร็จ Terminal จะขึ้นข้อความประมาณ:

```text
โหลด cogs.general แล้ว
โหลด cogs.announcements แล้ว
โหลด cogs.meetings แล้ว
โหลด cogs.attendance แล้ว
โหลด cogs.tasks แล้ว
ซิงก์คำสั่งในเซิร์ฟเวอร์แล้ว ...
เข้าสู่ระบบเป็น AFT.SBTVC (...)
```

จากนั้นบอทควรเปลี่ยนเป็น Online ใน Discord

## Discord Bot Permissions ที่แนะนำ

เปิดเฉพาะที่จำเป็น:

- View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Add Reactions
- Use Application Commands

ไม่แนะนำให้เปิด **Administrator**

## Privileged Gateway Intents

เวอร์ชันปัจจุบันไม่ต้องใช้:

- Presence Intent
- Server Members Intent
- Message Content Intent

จึงสามารถปิดไว้ทั้งหมดได้

## การเปิดบอท 24/7

ไฟล์ `Procfile` เตรียมคำสั่ง Worker ไว้ให้แล้ว:

```text
worker: python main.py
```

เมื่อนำไป Deploy ให้ตั้ง Environment Variables บนผู้ให้บริการ Hosting แทนการอัปโหลดไฟล์ `.env`

## ความปลอดภัย

- ห้าม Commit Discord Bot Token
- หาก Token เคยหลุด ให้ Reset Token ใน Discord Developer Portal ทันที
- อย่าให้ Role ของบอทเป็น Administrator ถ้าไม่จำเป็น
- Database และไฟล์ Environment ถูก Ignore จาก Git แล้ว
