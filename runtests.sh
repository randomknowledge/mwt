#!/bin/sh
pep8 --exclude=migrations --ignore=E501,E225,E121,E123,E124,E125,E127,E128 mwt || exit 1
pyflakes -X mwt/migrations mwt || exit 1