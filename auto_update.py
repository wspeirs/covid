import requests
import subprocess

from datetime import datetime
from os.path import join

BASE_PATH='/home/wspeirs/src/covid/'


def log(message):
    with open(join(BASE_PATH, 'auto_update.log'), 'a') as f:
        f.write("{}:\t".format(datetime.now()))
        f.write(message)
        f.write("\n")


# look to see if we have a new SHA for HEAD of the NYTs repo
res = requests.get('https://api.github.com/repos/nytimes/covid-19-data/commits/HEAD')

if res.status_code != 200:
    log("BAD STATUS CODE: {}".format(res.status_code))
    exit(-1)

json = res.json()

current_commit = str(json['sha'])

log('CUR SHA: {}'.format(current_commit))

with open(join(BASE_PATH, 'head.sha'), 'r') as f:
    last_sha = f.readline()

if last_sha.strip().lower() == current_commit.strip().lower():
    log('SAME SHA')
    exit(0)

log('NEW SHA: {}'.format(last_sha))

# we found a new commit, so run our update script and update the file
rc = subprocess.call(join(BASE_PATH, "run.sh"), shell=True)

log('RET CODE: {}'.format(rc))

with open(join(BASE_PATH, 'head.sha'), 'w') as f:
    f.writelines(current_commit.strip().lower())

