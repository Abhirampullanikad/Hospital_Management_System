<h1 align="center">🏥 Hospital Management System</h1>

<p align="center">
  <b>Role-based web application for Hospitals</b><br/>
  <i>Manage appointments, doctors, patients & more — with Django + AWS EC2</i><br/><br/>
  🔗 <a href="http://54.175.74.173" target="_blank"><strong>🌐 Live Demo</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Cloud-AWS_EC2-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-Bootstrap_5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

---

✨ Overview

🚀 **Hospital Management System** is a robust, responsive web app designed to handle the administrative tasks of a hospital through 3 major user roles:

- 👑 **Admin** – Manages doctors, patients, appointments & departments,Generate Bill
- 🩺 **Doctor** – Views schedule, patient history, and updates records,Generate prescription
- 👤 **Patient** – Books appointments, views status & history, Download Bill in PDF format, Pay bill, Download prescription

🎯 Built with **Django**, styled using **Bootstrap 5** **HTML** **CSS**, and deployed on **AWS EC2** for high availability and performance.

---

🧩 Key Features

- 🔐 Secure role-based login & dashboards
- 📅 Appointment scheduling & tracking
- 📊 Graphical stats for admins (patients/doctors/appointments)
- 📁 Manage departments & doctor-patient assignments
- 🧠 Scalable & extensible architecture
- 🖥️ Responsive design – mobile and desktop friendly

---

🔐 Demo Credentials

| Role     | Username | Password   |
|----------|----------|------------|
| 👑 Admin | admin1    | abhi6282413470   |
| 🩺 Doctor | doc1     | docpass    |
| 👤 Patient | pat1     | patpass    |

---

🛠️ Tech Stack

| Layer         | Tech                                                                 |
|---------------|----------------------------------------------------------------------|
| ⚙️ Backend    | Django Python |
| 🎨 Frontend   | Bootstrap, HTML5, CSS3 |
| 🛢️ Database   | SQLite |
| ☁️ Deployment | AWS EC2 Ubuntu Server |
| 🌐 Web Server | Gunicorn + Nginx                                           |

---

📦 Project Structure

```bash
hospital/
├── core/              # Main app (views, models, urls)
├── templates/         # HTML templates
├── static/            # CSS, JS, Images
├── media/             # Uploaded files (optional)
├── manage.py
└── requirements.txt
🧪 Installation Guide
🔧 Prerequisites
Python 3.8+

pip + virtualenv

Git

⚙️ Steps
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/your-username/hospital-management.git
cd hospital-management

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
🔗 Visit: http://127.0.0.1:8000
```
☁️ Deployment on AWS EC2

✅ The app is live at: http://54.175.74.173
Deployed using Ubuntu, served with Gunicorn and optionally reverse-proxied via Nginx.

Want a guide on how to deploy this on EC2? Just ask! 🧑‍💻

🎯 Future Enhancements

📧 Email/SMS notifications

📄 Medical records upload/download

📱 Mobile App integration (via Django REST API)



🙋‍♂️ Author
Built with ❤️ by Abhiram

🔗 Linkdin: www.linkedin.com/in/abhiram-p-29369b314

📧 Email: abhiramppullanikad23@gmail.com

📜 License
This project is licensed under the MIT License.

⭐ Star this repository to support the project and follow for updates!

markdown
Copy
Edit

---

##🚀 Django Deployment on AWS EC2 (Ubuntu)

##🌐 Live Site Example: http://54.175.74.173

✅ Prerequisites
EC2 Ubuntu instance running

SSH access to EC2

Django project uploaded (via Git or SCP)

Domain (optional)

Ports 22 (SSH), 80 (HTTP) allowed in EC2 security group

📦 Step 1: SSH into EC2
bash
Copy
Edit
ssh -i your-key.pem ubuntu@your-ec2-ip

⚙️ Step 2: Install System Dependencies

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y

🛠️ Step 3: Clone Your Project

cd /home/ubuntu
git clone https://github.com/your-username/hospital-management.git
cd hospital-management

🧪 Step 4: Set Up Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

🔐 Step 5: Configure Django for Production
In settings.py:
DEBUG = False
ALLOWED_HOSTS = ['54.175.74.173', 'yourdomain.com']
python
Copy
Edit
STATIC_ROOT = BASE_DIR / 'staticfiles'
Then collect static files:
python manage.py collectstatic

🧰 Step 6: Apply Migrations and Create Superuser

python manage.py migrate
python manage.py createsuperuser

🚦 Step 7: Test with Gunicorn
Install:

pip install gunicorn
Test locally:

gunicorn hospital.wsgi:application
Stop with CTRL+C.

🧱 Step 8: Set Up Gunicorn as a System Service
Create /etc/systemd/system/gunicorn.service:

sudo nano /etc/systemd/system/gunicorn.service
Paste:

[Unit]
Description=gunicorn daemon for Hospital Management
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/hospital-management
ExecStart=/home/ubuntu/hospital-management/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/hospital-management/hospital.sock hospital.wsgi:application

[Install]
WantedBy=multi-user.target
Enable and start:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

🌐 Step 9: Configure Nginx
Create a config file:

sudo nano /etc/nginx/sites-available/hospital
Paste:

server {
    listen 80;
    server_name 54.175.74.173;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/hospital-management;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/hospital-management/hospital.sock;
    }
}
Enable site and restart Nginx:


sudo ln -s /etc/nginx/sites-available/hospital /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

🔐 Step 10: Allow Traffic on Port 80
Make sure your EC2 instance’s security group allows Inbound HTTP (port 80).

✅ Optional: Enable HTTPS with Let’s Encrypt

sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
🎉 Done!

Your Django app should now be live at:
👉 http://54.175.74.173

🧼 Bonus: Useful Commands

Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

View logs
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
