# Collection Tools

## Setup for the DB
#### apt-get
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
```
#### yum
```
sudo yum install mysql-server
sudo yum install mysql-devel
```
#### MySQL
```
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
pip install -r requirements.txt
```

## Execute code

python comParser.py
