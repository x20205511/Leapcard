
#Run the application

sudo chmod -R 775 /home/ubuntu/leapcard/myproj

cd /home/ubuntu/leapcard
python3 -m venv venv
source /home/ubuntu/leapcard/venv/bin/activate

cd /home/ubuntu/leapcard/myproj
pip install -r requirements.txt

sudo chown ubuntu:ubuntu *
cd /home/ubuntu/leapcard/myproj/application

sudo chown ubuntu:ubuntu *

echo "Running the application"
cd /home/ubuntu/leapcard/myproj
python3 application.py >> /dev/null 2>&1 &

