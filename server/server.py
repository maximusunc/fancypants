#!/usr/bin/env python
"""CLI for encoding/decoding Starbound player files."""
from collections import namedtuple
from datetime import datetime
import os
from shutil import copyfile
from typing import List

from fastapi import FastAPI
import starbound
from starlette.middleware.cors import CORSMiddleware

APP = FastAPI(
    title='Starbound Modder',
    version='1.0.0',
)

# enable CORS
APP.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    return player


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


@APP.get('/decode/{player_id}')
def decode_player(player_id: str):
    """Recieve the player_id from UI."""
    player = decode(player_id)
    return player


@APP.post('/encode/{player_id}')
def encode_player(player_id: str, player: List):
    """Recieve the player_id from UI."""
    encode(player_id, player)
    return 'Success'
