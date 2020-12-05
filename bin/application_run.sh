cd /home/ec2-user/vycai/proj

export PATH=/home/ec2-user/.local/bin:usr/bin:/usr/bin/python3:$PATH
sudo python3 -m pip install -r requirements.txt

gunicorn --bind 0.0.0.0:3501 wsgi:app --daemon
