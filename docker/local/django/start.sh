#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Veritabanı migrate
python manage.py migrate --no-input

# Static dosyaları topla
python manage.py collectstatic --no-input

# Django server'ı hosttan erişilebilir şekilde başlat
exec python manage.py runserver 0.0.0.0:8000
