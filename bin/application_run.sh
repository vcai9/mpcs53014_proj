cd /home/ec2-user/vycai/proj || exit

while :
  do
    pipenv run gunicorn --bind 0.0.0.0:3009 wsgi:app
    sleep 1
  done
