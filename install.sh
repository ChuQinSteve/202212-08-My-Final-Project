sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo pip3 install -r requirements.txt
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install nodejs
sudo apt install build-essential
sleep 5
if [node --version] && [npm --version]; then
    cd front-end && npm install && cd ..
fi
sudo npm install -g pm2