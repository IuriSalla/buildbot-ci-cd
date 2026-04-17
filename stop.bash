#!/bin/bash

# Venv
source venv/bin/activate

# Stop the buildbot server
buildbot stop master

# Stop the buildbot worker
buildbot-worker stop worker