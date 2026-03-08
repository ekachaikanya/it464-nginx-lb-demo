import os
import socket
from flask import Flask, jsonify, request

app = Flask(__name__)

SERVER_NAME  = os.getenv('SERVER_NAME', 'Unknown Server')
SERVER_COLOR = os.getenv('SERVER_COLOR', '#ffffff')
HOSTNAME     = socket.gethostname()
request_count = 0

# ────────────────────────────────────────────────────────────
# GET / — แสดงว่า request นี้ไปถึง server ไหน
# ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    global request_count
    request_count += 1

    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    forwarded_for = request.headers.get('X-Forwarded-For', '-')

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SERVER_NAME}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'JetBrains Mono', 'Courier New', monospace;
      background: #060b14;
      color: #c8d8f0;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }}
    .card {{
      text-align: center;
      padding: 50px 60px;
      border: 2px solid {SERVER_COLOR};
      border-radius: 20px;
      background: #0d1626;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 0 40px {SERVER_COLOR}33;
      animation: appear 0.3s ease;
    }}
    @keyframes appear {{
      from {{ transform: scale(0.95); opacity: 0; }}
      to   {{ transform: scale(1); opacity: 1; }}
    }}
    .server-icon {{ font-size: 3.5rem; margin-bottom: 20px; }}
    h1 {{ color: {SERVER_COLOR}; font-size: 1.8rem; margin-bottom: 8px; }}
    .badge {{
      display: inline-block;
      background: {SERVER_COLOR}22;
      border: 1px solid {SERVER_COLOR}55;
      color: {SERVER_COLOR};
      padding: 4px 12px;
      border-radius: 999px;
      font-size: 0.75rem;
      margin-bottom: 24px;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 20px 0;
      text-align: left;
    }}
    .info-item {{
      background: #060b14;
      border: 1px solid #1e3050;
      border-radius: 8px;
      padding: 12px;
    }}
    .info-label {{ color: #546e7a; font-size: 0.7rem; margin-bottom: 4px; }}
    .info-value {{ color: #fff; font-size: 0.85rem; word-break: break-all; }}
    .tip {{
      margin-top: 24px;
      color: #546e7a;
      font-size: 0.78rem;
      border-top: 1px solid #1e3050;
      padding-top: 16px;
    }}
    .tip span {{ color: {SERVER_COLOR}; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="server-icon">⚡</div>
    <h1>{SERVER_NAME}</h1>
    <div class="badge">Load Balanced by Nginx</div>

    <div class="info-grid">
      <div class="info-item">
        <div class="info-label">HOSTNAME</div>
        <div class="info-value">{HOSTNAME}</div>
      </div>
      <div class="info-item">
        <div class="info-label">REQUEST #</div>
        <div class="info-value">{request_count}</div>
      </div>
      <div class="info-item">
        <div class="info-label">CLIENT IP</div>
        <div class="info-value">{client_ip}</div>
      </div>
      <div class="info-item">
        <div class="info-label">X-Forwarded-For</div>
        <div class="info-value">{forwarded_for}</div>
      </div>
    </div>

    <div class="tip">
      🔄 กด <span>F5</span> ซ้ำๆ เพื่อดู Load Balancing ในแอคชัน!<br>
      Request จะถูกส่งไปยัง Server 1, 2, 3 วนเวียนกัน
    </div>
  </div>
</body>
</html>"""
    return html


# ────────────────────────────────────────────────────────────
# GET /health — Health check endpoint
# ────────────────────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'server': SERVER_NAME,
        'hostname': HOSTNAME,
        'requests_served': request_count
    })


if __name__ == '__main__':
    print(f"🚀 Starting {SERVER_NAME} on :5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
