CONFIG_FILE="config.py"

function getvar()
{
    grep -oP "${1}\s*=\s*[\"']\K.+(?=[\"'])" ${CONFIG_FILE}
}

STORAGE_DIR=$(getvar "STORAGE_DIR")
CAPTURES_DIR=$(getvar "CAPTURES_DIR")

echo "Creating directory ${STORAGE_DIR} for peristent key-value storage"
mkdir -p ${STORAGE_DIR}
echo "Creating directory ${CAPTURES_DIR} for camera captures"
mkdir -p ${CAPTURES_DIR}
