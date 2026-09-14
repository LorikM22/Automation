#!/bin/bash
if [ $# -lt 1 ]; then
        echo "!Specifica calea catre director!"
        echo "Exemplu: ./cleanup.sh <director> [extensie] [extensie] ..."
        exit 1
fi

DIRECTORY="$1"

if [ ! -d "$DIRECTORY" ]; then
        echo "Eroare: directorul '$DIRECTORY' nu există."
        exit 1
fi

if [ $# -eq 1 ]; then
        EXTENSIONS=(".tmp")
else
        EXTENSIONS=("${@:2}")
fi

DELETED_COUNT=0

for EXTENSION in "${EXTENSIONS[@]}"; do
        while IFS= read -r -d '' FILE; do
                rm "$FILE"
                DELETED_COUNT=$((DELETED_COUNT + 1))
        done < <(find "$DIRECTORY" -type f -name "*$EXTENSION" -print0)
done

echo "Au fost șterse $DELETED_COUNT fișiere."
