#!/usr/bin/env python
"""
phpIPAM.py: Manage phpIPAM
"""

import argparse
# import csv
import json
import requests
# from requests.auth import HTTPBasicAuth

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr

class phpIPAM(object):
    def __init__(self):
        self.read_cli_args()
        self.actions()

    def actions(self):
        if self.args.action == "auth":
            self.auth()
        elif self.args.action == "query_sections":
            self.query_sections()
        elif self.args.action == "query_subnets":
            self.query_subnets()
        elif self.args.action == "show_sections":
            self.show_sections()

    def auth(self):
        url = self.args.apiurl+"/api/"+self.args.appid+"/user/"
        request = requests.post(url, auth=(self.args.username, self.args.password))
        response = request.json()
        print json.dumps(response, indent=4)
        # self.auth_token = response["data"]["token"] # Not used yet...May be used to proceed with auth after logging in
        # print self.auth_token

    def query_sections(self):
        headers = {'token': self.args.apitoken}
        url = self.args.apiurl+"/api/"+self.args.appid+"/sections/"
        request = requests.get(url, headers=headers)
        response = request.json()
        if self.args.sectionname is None:
            print json.dumps(response, indent=4)
        elif self.args.sectionname is not None:
            for key in response["data"]:
                sectionId = key["id"]
                sectionName = key["name"]
                if self.args.sectionname == sectionName:
                    url = self.args.apiurl+"/api/"+self.args.appid+"/sections/"+sectionId+"/"
                    request = requests.get(url, headers=headers)
                    response = request.json()
                    print json.dumps(response, indent=4)

    def query_subnets(self):
        headers = {'token': self.args.apitoken}
        url = self.args.apiurl+"/api/"+self.args.appid+"/sections/"
        request = requests.get(url, headers=headers)
        response = request.json()
        subnets_found = False
        for key in response["data"]:
            sectionId = key["id"]
            sectionName = key["name"]
            if self.args.sectionname == sectionName:
                url = self.args.apiurl+"/api/"+self.args.appid+"/sections/"+sectionId+"/subnets/"
                request = requests.get(url, headers=headers)
                response = request.json()
                print json.dumps(response, indent=4)
                subnets_found = True
        if not subnets_found:
            print "Subnets not found for section name "+"'"+self.args.sectionname+"'"

    def show_sections(self):
        headers = {'token': self.args.apitoken}
        url = self.args.apiurl+"/api/"+self.args.appid+"/sections/"
        request = requests.get(url, headers=headers)
        response = request.json()
        sections = {}
        sections['data'] = {}
        sections['data']['sections'] = {}
        for key in response["data"]:
            sectionId = key["id"]
            sectionName = key["name"]
            sections['data']['sections'][sectionName] = sectionId
        print json.dumps(sections, indent=4)

    def read_cli_args(self):
        """
        Read variables from CLI

        Read CLI variables passed on CLI
        """
        parser = argparse.ArgumentParser(description='phpIPAM Management...')
        parser.add_argument('action', help='Define action to take',
                            choices=['auth', 'query_sections', 'query_subnets', 'show_sections'])
        parser.add_argument('--apikey', help='API Key')
        parser.add_argument('--apitoken', help='API Token')
        parser.add_argument('--apiurl', help='API URL', default='http://127.0.0.1/phpipam')
        parser.add_argument('--appid', help='App Id')
        parser.add_argument('--password', help='API Password')
        parser.add_argument('--sectionname', help='Define section name')
        parser.add_argument('--username', help='API User')
        self.args = parser.parse_args()
        if self.args.appid is None:
            parser.error("Your application ID must be provided")
        if self.args.action != "auth" and self.args.apitoken is None:
            parser.error("Your API token must be provided")
        if self.args.action == "query_subnets" and self.args.sectionname is None:
            parser.error("A section name must be defined")

if __name__ == '__main__':
    phpIPAM()
