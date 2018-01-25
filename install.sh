#!/bin/bash

# make the config file if it doesn't exist
if [ ! -f $CONF_DIR/config.json ]; then
	cp $PKG_DIR/macro-kbd/config.json $CONF_DIR
fi
