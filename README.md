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
├── Dockerfile
├── .dockerignore
├── railway.json
├── Procfile
├── .python-version
├── .env.example
├── .gitignore
├── DEPLOY.md
├── README.md
├── .github/
│   └── workflows/
│       └── python-check.yml
└── cogs/
    ├── __init__.py
    ├── general.py
    ├── announcements.py
    ├── meetings.py
    ├── attendance.py
    └── tasks.py
```

ฐานข้อมูลใช้ **SQLite** และสร้างให้อัตโนมัติเมื่อบอทเริ่มทำงานครั้งแรก

- Local: ใช้ `./aft_sbtvc.db`
- Railway: ถ้ามี Volume บอทจะตรวจ `RAILWAY_VOLUME_MOUNT_PATH` และเก็บฐานข้อมูลบน Volume อัตโนมัติ
- สามารถกำหนดเองด้วย `DATABASE_PATH`

## รันบนเครื่อง

ต้องมี Python 3.12

```powershell
git clone https://github.com/SBTVC/AFT.SBTVC_BOT.git
cd AFT.SBTVC_BOT

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Copy-Item .env.example .env
```

แก้ไฟล์ `.env`

```env
DISCORD_TOKEN=ใส่_BOT_TOKEN_ตรงนี้
DISCORD_GUILD_ID=ใส่_SERVER_ID_AFT_SBTVC_ตรงนี้
```

จากนั้น:

```powershell
python main.py
```

## Deploy 24/7

Repo นี้เตรียม **Dockerfile + Railway Config** ไว้แล้ว

อ่านขั้นตอนที่:

- [DEPLOY.md](DEPLOY.md)

สิ่งสำคัญตอน Deploy:

1. ตั้ง `DISCORD_TOKEN` เป็น Secret/Variable บน Hosting
2. ตั้ง `DISCORD_GUILD_ID`
3. ถ้าใช้ SQLite ต้องต่อ Persistent Volume เพื่อไม่ให้ข้อมูลหายตอน Redeploy
4. ไม่ต้องเปิด Public Networking เพราะ Discord Bot เป็น Worker
5. ใช้ 1 replica เท่านั้นเมื่อใช้ SQLite

## Discord Bot Permissions ที่แนะนำ

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

## ความปลอดภัย

- ห้าม Commit Discord Bot Token
- หาก Token เคยหลุด ให้ Reset Token ใน Discord Developer Portal ทันที
- อย่าให้ Role ของบอทเป็น Administrator ถ้าไม่จำเป็น
- `.env` และไฟล์ฐานข้อมูลถูก Ignore จาก Git แล้ว
