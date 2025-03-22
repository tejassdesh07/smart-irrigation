# Smart Irrigation Django App

## Setup Instructions

### 1. Clone the Repository
```sh
cd /home/dteforms/smart-irrigation
git clone <repository_url>
cd DTE
```

### 2. Create and Activate Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### 5. Collect Static Files
```sh
python manage.py collectstatic --noinput
```

### 6. Run the Application Locally (Optional)
```sh
python manage.py runserver
```

---

## Deployment Instructions

### 1. Configure Nginx
Edit the Nginx configuration file:
```sh
sudo nano /etc/nginx/sites-enabled/irrigationform
```
Ensure it contains:
```nginx
server {
    listen 80;
    server_name 160.153.175.117 irrigationform.dtelandscape.com;
    location /static/ {
        alias /home/dteforms/smart-irrigation/DTE/static/;
    }

    location / {
        proxy_pass http://unix:/home/dteforms/smart-irrigation/DTE/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_log  /var/log/nginx/irrigationform_error.log;
    access_log /var/log/nginx/irrigationform_access.log;
}
```

Test Nginx configuration:
```sh
sudo nginx -t
```
Restart Nginx:
```sh
sudo systemctl restart nginx
```

Check Nginx status:
```sh
sudo systemctl status nginx
```

Reload Nginx (if necessary):
```sh
sudo systemctl reload nginx
```

To open the Nginx config file:
```sh
sudo nano /etc/nginx/sites-enabled/irrigationform
```

---

### 2. Configure Gunicorn
Edit the Gunicorn service file:
```sh
sudo nano /etc/systemd/system/gunicorn.service
```
Ensure it contains:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=dteforms
Group=www-data
WorkingDirectory=/home/dteforms/smart-irrigation/DTE
ExecStart=/home/dteforms/smart-irrigation/DTE/venv/bin/gunicorn --workers 3 --bind unix:/home/dteforms/smart-irrigation/DTE/gunicorn.sock DTE.wsgi:application
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Reload and restart Gunicorn:
```sh
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Check Gunicorn status:
```sh
sudo systemctl status gunicorn
```

Enable Gunicorn to start on boot:
```sh
sudo systemctl enable gunicorn
```

To open the Gunicorn service file:
```sh
sudo nano /etc/systemd/system/gunicorn.service
```

---

## Managing Services

### Start Gunicorn
```sh
sudo systemctl start gunicorn
```

### Stop Gunicorn
```sh
sudo systemctl stop gunicorn
```

### Restart Gunicorn
```sh
sudo systemctl restart gunicorn
```

### Check Gunicorn Status
```sh
sudo systemctl status gunicorn
```

### Start Nginx
```sh
sudo systemctl start nginx
```

### Stop Nginx
```sh
sudo systemctl stop nginx
```

### Restart Nginx
```sh
sudo systemctl restart nginx
```

### Reload Nginx (for config changes without stopping the service)
```sh
sudo systemctl reload nginx
```

### Check Nginx Status
```sh
sudo systemctl status nginx
```

---

## Logs and Debugging

### Check Gunicorn Logs
```sh
sudo journalctl -u gunicorn -n 100 --no-pager
```

### Check Nginx Logs
```sh
sudo journalctl -u nginx -n 100 --no-pager
```

### Monitor Nginx Errors in Real-time
```sh
sudo tail -f /var/log/nginx/error.log
```

### Monitor Gunicorn Errors in Real-time
```sh
sudo tail -f /var/log/syslog | grep gunicorn
```

### Restart All Services (if required)
```sh
sudo systemctl restart gunicorn nginx
```

---

## File Permissions
Ensure the correct permissions for Gunicorn and Nginx to access project files:
```sh
sudo chown -R dteforms:www-data /home/dteforms/smart-irrigation/
sudo chmod -R 755 /home/dteforms/smart-irrigation/
```

If permission issues persist, try:
```sh
sudo chmod -R 775 /home/dteforms/smart-irrigation/
sudo chmod -R g+s /home/dteforms/smart-irrigation/
```

To allow Nginx to access static files:
```sh
sudo chmod -R 755 /home/dteforms/smart-irrigation/DTE/static/
```

