# Collection Tools

## Setup for the DB

```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
mysql -u root -p
mysql> CREATE DATABASE com;
mysql> GRANT ALL PRIVILEGES ON com.* TO "dns"@"localhost" IDENTIFIED BY "password";
mysql> FLUSH PRIVILEGES;
mysql> EXIT
```

## Setup for virtualenv

```
sudo pip install virtualenv
mkdir ~/virtualenvs
virtualenv ~/virtualenvs/dns-tools
source ~/virtualenvs/dns-tools/bin/activate
pip install requirements.txt
```

## Execute code

python comParser.py
