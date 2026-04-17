#!/bin/bash

# Venv
source venv/bin/activate

# Start the buildbot server
buildbot start master

# Start the buildbot web server
buildbot-worker start worker