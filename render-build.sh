#!/usr/bin/env bash
# Hata oluşursa dur
set -o errexit

pip install -r requirements.txt
playwright install chromium
