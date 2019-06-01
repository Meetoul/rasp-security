#!/bin/bash

if ! [ -x "$(command -v python3)" ]; then
    echo "Error, python3 is not installed"
    exit 1
fi

INSTALLED_PACKAGES="$(pip3 freeze)"
REQUIREMENTS_FILE="requirements.txt"

grep -v "^#" ${REQUIREMENTS_FILE} | while read pkg; do
    echo "${INSTALLED_PACKAGES}" | grep "${pkg}" > /dev/null 2>&1
    if ! [ $? -eq 0 ]; then
        echo "Python package ${pkg} is not installed."
        not_satisfied=true
    fi
done

if ${not_satisfied}; then
    echo "You should run pip3 -r ${REQUIREMENTS_FILE} before running this script"
    exit 1
fi

CONFIG_FILE="config.py"

STORAGE_DEFAULT_DIR='storage'
CAPTURES_DEFAULT_DIR='captures'
LOGS_DEFAULT_DIR='log'
RECORDS_DEFAULT_DIR='records'

function getvar()
{
    grep -oP "^${1}\s*=\s*[\"']\K.+(?=[\"'])" ${CONFIG_FILE} 2>/dev/null
}

STORAGE_DIR="$(getvar "STORAGE_DIR" || echo "${STORAGE_DEFAULT_DIR}")"
CAPTURES_DIR="$(getvar "CAPTURES_DIR" || echo "${CAPTURES_DEFAULT_DIR}")"
LOGS_DIR="$(getvar "LOGS_DIR" || echo "${LOGS_DEFAULT_DIR}")"
RECORDS_DIR="$(getvar "RECORDS_DIR" || echo "${RECORDS_DEFAULT_DIR}")"

echo "Creating directory ${STORAGE_DIR} for peristent key-value storage"
mkdir -p "${STORAGE_DIR}"
echo "Creating directory ${CAPTURES_DIR} for camera captures"
mkdir -p "${CAPTURES_DIR}"
echo "Creating directory ${LOGS_DIR} for log records"
mkdir -p "${LOGS_DIR}"
echo "Creating directory ${RECORDS_DIR} for webcam records"
mkdir -p "${RECORDS_DIR}"
