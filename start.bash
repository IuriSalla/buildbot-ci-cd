#!/bin/bash

ln -snf /usr/local/src/buildbot/buildbot /usr/local/src/buildbot/master/scripts

# Venv
source venv/bin/activate

# Start the buildbot server
buildbot start master

# Start the buildbot web server
buildbot-worker start worker
