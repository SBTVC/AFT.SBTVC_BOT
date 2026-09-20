# Deploy AFT.SBTVC_BOT แบบ 24/7

คู่มือนี้ใช้ Railway เป็นตัวอย่าง เพราะเชื่อม GitHub, รองรับ Docker และตั้ง Environment Variables ได้ง่าย

## 1. สร้าง Project บน Railway

1. เข้า Railway
2. สร้าง New Project
3. เลือก Deploy from GitHub Repo
4. เลือก `SBTVC/AFT.SBTVC_BOT`

Railway จะอ่าน `Dockerfile` และ `railway.json` จาก repo

## 2. ตั้ง Variables

เพิ่ม:

```text
DISCORD_TOKEN=Bot Token จาก Discord Developer Portal
DISCORD_GUILD_ID=Server ID ของ AFT-SBTVC
```

ห้าม Commit Token ลง GitHub

## 3. เพิ่ม Persistent Volume

บอทใช้ SQLite ดังนั้นต้องมีพื้นที่เก็บข้อมูลถาวร

สร้าง Volume แล้ว Mount เข้า Service

ตัวบอทตรวจ `RAILWAY_VOLUME_MOUNT_PATH` อัตโนมัติ และจะเก็บไฟล์:

```text
<volume mount path>/aft_sbtvc.db
```

ถ้าต้องการกำหนดเองสามารถเพิ่ม:

```text
DATABASE_PATH=/data/aft_sbtvc.db
```

และ Mount Volume ที่ `/data`

## 4. ไม่ต้องเปิด Public Networking

Discord Bot เชื่อมออกไปหา Discord Gateway เอง จึงไม่จำเป็นต้องมีโดเมนหรือ HTTP Port สำหรับเวอร์ชันนี้

## 5. Deploy

หลังตั้ง Variables และ Volume แล้ว ให้ Deploy Service

ใน Logs ควรเห็นประมาณ:

```text
โหลด cogs.general แล้ว
โหลด cogs.announcements แล้ว
โหลด cogs.meetings แล้ว
โหลด cogs.attendance แล้ว
โหลด cogs.tasks แล้ว
ซิงก์คำสั่งในเซิร์ฟเวอร์แล้ว ...
เข้าสู่ระบบเป็น AFT.SBTVC (...)
```

จากนั้น Bot ใน Discord ควรขึ้น Online

## 6. ทดสอบ

ลอง:

```text
/ทดสอบ
/ช่วยเหลือ
/ประกาศ
/ประชุม สร้าง
/เช็กชื่อ เปิด
/งาน เพิ่ม
```

## 7. สำคัญสำหรับ SQLite

ใช้ Service เพียง 1 replica ขณะยังใช้ SQLite

ถ้าภายหลังต้องการ Scale หลาย instance ให้ย้ายฐานข้อมูลไป PostgreSQL/Supabase ก่อน

## 8. ถ้า Bot Offline

ตรวจตามลำดับ:

1. Deployment Logs
2. `DISCORD_TOKEN` ถูกต้องหรือไม่
3. `DISCORD_GUILD_ID` ถูกต้องหรือไม่
4. Bot ถูกเชิญเข้า Server แล้วหรือไม่
5. Discord Bot Permissions
6. Service ถูก Restart หรือ Crash หรือไม่

## 9. เปลี่ยน Token

ถ้า Token หลุด:

1. Discord Developer Portal → Bot
2. Reset Token
3. เปลี่ยน `DISCORD_TOKEN` บน Railway
4. Redeploy/Restart Service

ไม่ต้องแก้ Token ใน source code
