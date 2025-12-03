# 🚀 Deployment Guide (Flask App Factory)

## 1. Server Prep (Ubuntu)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-venv python3-pip nginx ufw -y
```

## 2. Clone & Setup
```bash
cd /opt
sudo git clone pragneshraval288-create/SmartDMS Smartdms
cd Smartdms
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

## 3. Permissions
```bash
sudo chown -R www-data:www-data instance/
sudo chmod -R 775 instance/
```

## 4. Systemd Service (Gunicorn)
Create service:
```ini
[Unit]
Description=SmartDMS Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/Smartdms
EnvironmentFile=/opt/Smartdms/.env
ExecStart=/opt/Smartdms/venv/bin/gunicorn -w 3 -b 127.0.0.1:8001 "backend.app:create_app()"
Restart=always

[Install]
WantedBy=multi-user.target
```
Start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable smartdms
sudo systemctl start smartdms
sudo systemctl status smartdms
```

## 5. Nginx Config
```nginx
server {
    listen 80;
    server_name _;
    location /static/ { alias /opt/Smartdms/frontend/static/; }
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```
Activate:
```bash
sudo ln -s /etc/nginx/sites-available/smartdms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. HTTPS (Certbot)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
sudo certbot renew --dry-run
```

## 7. Firewall
```bash
sudo ufw enable
sudo ufw allow "Nginx Full"
sudo ufw status
```

##  Access
```
https://yourdomain.com/dashboard
https://yourdomain.com/documents
https://yourdomain.com/login
```