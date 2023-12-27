#!/bin/python3

#####################################################################
## Watch a log file for new lines and match strings.               ##
## Specify ignore time to not repeat action for period.            ##
## If all strings are matched in line perform an HTTP get request. ##
#####################################################################

import time
import argparse
import io
import requests

class Parse:

    def __init__(self, line, session):

        self.line = line
        self.session = session
    
    def __parse(self):
        
        if all(e in self.line for e in self.session.args.conditions):

            if time.time() - self.session.get_timectl() > self.session.args.ignore * 60:

                self.session.set_timectl(time.time())
                print("DO SOMETHING NOW!")
                requests.get(self.session.args.uri)

    def __request(self):

        requests.post(self.session.args.uri)                
    
    def parse(self):

        self.__parse()

class Session:

    def __init__(self, arg_parser):

        self.arg_parser = arg_parser
        self.args = self.__parse_args()
        self.log = io.open(self.args.log)
        self.timectl = 0

    def __parse_args(self):

        self.arg_parser.add_argument("-l", "--log", type=str, required=True, help="log file to watch")
        self.arg_parser.add_argument("-c", "--conditions", type=str, nargs="+", required=True, help="conditions to match in new log lines, if all conditions are matched the action is performed")
        self.arg_parser.add_argument("-i", "--ignore", type=int, required = True, help="period in minutes to ignore additional matches")
        self.arg_parser.add_argument("-u", "--uri", type=str, required = True, help="uri for http request")
       
        return self.arg_parser.parse_args()

    def __monitor(self):

        self.log.seek(0, 2)

        while True:
            line = self.log.readline()
            if line:
                Parse(line, self).parse()
            else:
                time.sleep(1)

    def get_timectl(self):

        return self.timectl

    def set_timectl(self, time):

        self.timectl = time

    def run(self):

        self.__monitor()

def main():

    session = Session(argparse.ArgumentParser())
    session.run()

if __name__ == "__main__":

    main()
