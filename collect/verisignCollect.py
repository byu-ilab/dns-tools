import argparse
import datetime
import os
import sys
import traceback

from ftplib import FTP

class Collect:
    def __init__(self):
        self.options = self.parse_arguments()
        self.files = {'rz.verisign-grs.com':['com.zone.gz','net.zone.gz','root.zone.gz'],
                      'rzname.verisign-grs.com':['master.name.zone.gz']}
        self.dir_name = "%s/%s" % (self.options.directory,self.get_date())
        self.make_dir()
        self.download_files()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(prog='verisignCollect', description='A script to collect registration data from Verisign', add_help=True)
        parser.add_argument('-d', '--directory', type=str, action='store', help='directory for storing registration data',default='.')
        parser.add_argument('-u', '--username', type=str, action='store', help='username for server',default='')
        parser.add_argument('-p', '--password', type=str, action='store', help='password for server',default='')
        return parser.parse_args()

    def get_date(self):
        today = datetime.date.today()
        return "%s-%s-%s" % (today.year,today.month,today.day)

    def make_dir(self):
        try:
            if not os.path.exists(self.dir_name):
                os.makedirs(self.dir_name)
        except:
            print traceback.format_exc()
            sys.exit()

    def download_files(self):
        for server in self.files.keys():
            for filename in self.files[server]:
                ftp = FTP(server)
                ftp.login(self.options.username,self.options.password)
                store = "%s/%s" % (self.dir_name,filename)
                ftp.retrbinary('RETR %s' % filename,open(store, 'wb').write)
                ftp.quit()
        

if __name__ == "__main__":
    c = Collect()

