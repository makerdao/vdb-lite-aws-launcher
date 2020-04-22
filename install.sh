#!/usr/bin/env bash
set -e
rm -rf .env
virtualenv .env
source .env/bin/activate
pip install $(cat requirements.txt)