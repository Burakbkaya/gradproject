#!/usr/bin/env bash
# Hata oluşursa dur
set -o errexit

pip install -r requirements.txt
playwright install chromium

# Modelin ilk istekte inmesini ve zaman aşımına sebep olmasını engellemek için build aşamasında indiriyoruz:
python -c "from transformers import pipeline; pipeline('sentiment-analysis', model='savasy/bert-base-turkish-sentiment-cased')"
