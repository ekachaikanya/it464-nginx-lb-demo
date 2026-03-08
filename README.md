# 🔄 Nginx Load Balancer Demo

> สาธิต Load Balancer + Reverse Proxy ด้วย Nginx บน Docker Compose

## 📁 โครงสร้างไฟล์

```
nginx-lb-demo/
├── docker-compose.yml        ← Main orchestration
├── nginx/
│   └── nginx.conf            ← Nginx: LB + Reverse Proxy config
└── app/
    ├── app.py                ← Flask app (แสดง server name)
    ├── Dockerfile
    └── requirements.txt
```

## 🚀 เริ่มใช้งาน

```bash
# 1. Build และ Start ทุก container
docker compose up --build -d

# 2. ดู status
docker compose ps

# 3. ทดสอบ Load Balancing
curl http://localhost:8080

# กด F5 ซ้ำๆ ใน browser หรือ:
for i in {1..9}; do
  curl -s http://localhost:8080 | grep -o 'App Server [0-9]'
done
```

## 🧪 ทดลองเพิ่มเติม

```bash
# ดู Nginx stats
curl http://localhost:8080/status

# Health check
curl http://localhost:8080/health

# ดู log realtime
docker compose logs -f nginx

# Scale app1 เป็น 2 instances
#docker compose up --scale app1=2 -d

# หยุด server 1 ดูว่า traffic failover ไปไหม
docker compose stop app1
curl http://localhost:8080   # ควรยังตอบสนองได้

# เริ่ม server 1 ใหม่
docker compose start app1

# หยุดทั้งหมด
docker compose down
```

## ⚙️ เปลี่ยน Algorithm

แก้ไขใน `nginx/nginx.conf` บรรทัด `upstream backend`:

| Algorithm | ใช้เมื่อ |
|-----------|----------|
| `least_conn` | Request มี duration ต่างกัน (default ใน demo) |
| `round_robin` | Request ใช้เวลาเท่ากัน (comment ทิ้ง least_conn) |
| `ip_hash` | ต้องการ session sticky |

จากนั้น reload config:
```bash
docker compose exec nginx nginx -s reload
```

## 🔍 Architecture

```
Browser → Nginx :80 (Load Balancer)
              ├── app1:5000 (Flask)
              ├── app2:5000 (Flask)
              └── app3:5000 (Flask)
```

ทุก app container อยู่ใน docker network `app-network` และ
ไม่ expose port ออกมาภายนอก — ต้องผ่าน Nginx เท่านั้น
