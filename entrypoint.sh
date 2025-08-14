#!/bin/bash

# run the post-init script in the root directory (i.e. coming from the image)
if [ -f "/post-init.sh" ]; then
    . /post-init.sh
fi

# run the post-init script in the project directory
if [ -f "./post-init.sh" ]; then
    . ./post-init.sh
fi

# Override the jupyter command to be forward compatible with newer
# images that no longer launch the whole server with `jupyter notebook`.
jupyter() {
    if [ "$1" = "notebook" ]; then
        shift
        $(which jupyter) server "$@"
    else
        $(which jupyter) "$@"
    fi
}

if [[ -v RENKU_BASE_URL_PATH ]]; then
    "$@" --ServerApp.port=8888 --ServerApp.base_url="$RENKU_BASE_URL_PATH" \
        --ServerApp.token="" --ServerApp.password="" --ServerApp.allow_remote_access=true \
        --ContentsManager.allow_hidden=true --ServerApp.allow_origin=* \
        --ServerApp.root_dir="${HOME}/lab/"
fi

# run the command
"$@"