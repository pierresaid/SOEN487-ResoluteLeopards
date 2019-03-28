#!/usr/bin/env bash

json+="[\n"

for i in {1..5}; do
    # Make up a name for the key
    d=$(date +"%Y-%m")
    name="Key-${d}-${i}"

    # Make a json to reference the keys
    if [[ $i -ne 1 ]]; then
        json+=",\n"
    fi
    json+="  {\"name\": \"$name\", \"path\": \"$(pwd)/$name.pem\"}"

    # Generate the key
    openssl genrsa -out "$name.pem" 2048

    echo "Generated key $name"
done

json+="\n]"

echo -e "$json" > "keylist.json"
