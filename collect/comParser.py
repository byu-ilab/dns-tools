import argparse
import datetime
import gzip
import sys
import traceback

from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *

Base = declarative_base()

from comConfig import *

class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    server = Column(String(256), index=True)
    start = Column(Date)
    end = Column(Date)

    @staticmethod
    def get_or_create(session, name, server, date):
        year,month,day = date.split('-')
        d = datetime.date(int(year),int(month),int(day))
        host = session.query(Host).filter_by(name=name,server=server).first()
        if host:
            if host.end - d == 1:
                # Same entry as previous one
                host.end = d
            else:
                # Previous entry expired, so this is a new entry even
                # if the name server is the same
                host = Host(name=name,server=server,start=d,end=d)
                session.add(host)
            return host
        else:
            host = Host(name=name,server=server,start=d,end=d)
            session.add(host)
            return host

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, index=True)
    kind = Column(String(10))
    address = Column(String(30))
    start = Column(Date)
    end = Column(Date)

    @staticmethod
    def get_or_create(session, name, kind, address, date):
        year,month,day = date.split('-')
        d = datetime.date(int(year),int(month),int(day))
        server = session.query(Server).filter_by(name=name,kind=kind,address=address).first()
        if server:
            if server.end - d == 1:
                # Same entry as previous one
                server.end = d
            else:
                # Previous entry expired, so this is a new entry even
                # if the address is the same
                server = Server(name=name,kind=kind,address=address,start=d,end=d)
                session.add(server)
            return host
        else:
            server = Server(name=name,kind=kind,address=address,start=d,end=d)
            session.add(server)
            return server

class DNSSEC(Base):
    __tablename__ = 'dnssecs'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), index=True)
    start = Column(Date)
    end = Column(Date)

    @staticmethod
    def get_or_create(session, name, date):
        year,month,day = date.split('-')
        d = datetime.date(int(year),int(month),int(day))
        dnssec = session.query(DNSSEC).filter_by(name=name).first()
        if dnssec:
            if dnssec.end - d == 1:
                # Same entry as previous one
                dnssec.end = d
            else:
                # Previous entry expired, so this is a new entry even
                # if the name is the same
                dnssec = DNSSEC(name=name,start=d,end=d)
                session.add(dnssec)
            return host
        else:
            dnssec = DNSSEC(name=name,start=d,end=d)
            session.add(dnssec)
            return dnssec

class comParser:
    def __init__(self):
        # parse options
        self.options = self.parse_arguments()
        if not self.options.date:
            self.date = self.get_date()
        else:
            self.date = self.options.date
        self.directory = "%s/%s" % (self.options.directory,self.date)
        # setup database
        self.setup_db()
        # parse COM
        self.parse('com.zone.gz')

    def parse_arguments(self):
        parser = argparse.ArgumentParser(prog='comParser', description='A script to parse domain registration data for .COM', add_help=True)
        parser.add_argument('-d', '--directory', type=str, action='store', help='directory where registration data is stored',default='.')
        parser.add_argument('--date', type=str, action='store', help='date to parse, in format of YYYY-MM-DD',default=None)
        return parser.parse_args()

    def get_date(self):
        today = datetime.date.today()
        return "%s-%s-%s" % (today.year,today.month,today.day)

    def setup_db(self):
        try:
            self.db = create_engine('mysql://%s:%s@%s' % (DB_USER,DB_PASSWORD,DB_SERVER))
            self.db.execute('USE %s' % (DB_NAME))
            Base.metadata.create_all(self.db)
            self.session = sessionmaker(bind=self.db)()
        except:
            print traceback.format_exc()
            sys.exit()

    def parse(self,filename):
        counter = 0
        with gzip.open('%s/%s' % (self.directory,filename),'r') as FILE:
            for line in FILE:
                counter += 1
                if counter == 10000:
                    self.session.commit()
                    counter = 0
                    import sys
                    sys.exit()
                fields = line.split()
                if len(fields) == 0:
                    continue
                if fields[0] == "COM.":
                    continue
                if len(fields) < 3:
                    continue
                if fields[1] == 'NS':
                    # check if host in DB and add if not
                    host = Host.get_or_create(self.session,fields[0],fields[2],self.date)
                    continue
                if fields[1] == 'A' or fields[1] == 'AAAA':
                    # check if NS in DB
                    server = Server.get_or_create(self.session,fields[1],fields[3],self.date)
                    continue
                if fields[2] == 'RRSIG':
                    dnssec = DNSSEC.get_or_create(self.session,fields[0],self.date)


if __name__ == "__main__":
    c = comParser()

