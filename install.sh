#!/bin/bash

# make the config file if it doesn't exist
if [ ! -f $CONF_DIR/macrokbd_config.json ]; then
	cp $PKG_DIR/macro-kbd/macrokbd_config.json $CONF_DIR
fi
