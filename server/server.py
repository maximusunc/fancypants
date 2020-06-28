#!/usr/bin/env python
"""CLI for encoding/decoding Starbound player files."""
import argparse
from collections import namedtuple
from datetime import datetime
import os
import json
from shutil import copyfile
import starbound
from flask import Flask, request
from flask_cors import CORS

app = Flask("starbound_modder")

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# 71db19adaa3ac911aaaf1792ab65856d.player

VersionedJSON = namedtuple('VersionedJSON', ['name', 'version', 'data'])


def get_player_dir():
    """Get player file directory."""
    home_dir = os.path.expanduser('~')
    return os.path.join(
        home_dir,
        'Library/Application Support/Steam/steamapps/common/',
        'Starbound/storage/player/',
    )


def uuid_to_file(player_uuid):
    """Get player file from uuid."""
    player_dir = get_player_dir()
    return os.path.join(
        player_dir,
        player_uuid + '.player',
    )


def decode(player_uuid):
    """Decode Starbound player file to JSON."""
    player_file = uuid_to_file(player_uuid)

    # load player file
    with open(player_file, 'rb') as f:
        player = starbound.read_sbvj01(f)

    return json.dumps(player)


def encode(player_uuid, player_obj):
    """Encode Starbound player file from JSON."""
    player_file = uuid_to_file(player_uuid)

    # backup player file
    backup_dir = os.path.join(
        get_player_dir(),
        'backup',
    )
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime('%y%m%d%H%M%S')
    backup_file = os.path.join(
        backup_dir,
        player_uuid + '.player' + '.backup' + timestamp,
    )
    copyfile(player_file, backup_file)

    # convert JSON to SBON
    player = VersionedJSON(*player_obj)

    # overwrite player file
    with open(player_file, 'wb') as fh:
        starbound.write_sbvj01(fh, player)


@app.route('/decode/<string:player_id>', methods=['GET'])
def decode_player(player_id):
    """Recieve the player_id from UI."""
    player = decode(player_id)
    return player, 200


@app.route('/encode/<string:player_id>', methods=['POST'])
def encode_player(player_id):
    """Recieve the player_id from UI."""
    player = request.json
    encode(player_id, player)
    return 'Success', 200


# def shutdown_server():
#     """Shut down the server after handling current requests."""
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running the server')
#     func()


# @app.route('/shutdown')
# def shutdown():
#     """Allow frontend to shut down server."""
#     shutdown_server()
#     return 'Server is shutting down...'


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5748,
        debug=False,
        use_reloader=False,
    )
