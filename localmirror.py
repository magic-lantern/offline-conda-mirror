# ## Development/Testing of Conda off-line tool
# 
# This notebook is automatically written as a Markdown file using https://github.com/mwouts/jupytext

import click
from conda.core.index import get_index
from conda.resolve import Resolve
import os
import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError
from pathlib import Path


#conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
#python mirror.py --output=pytorch.yaml --upstream-channel pytorch --upstream-channel defaults pytorch torchvision "cudatoolkit=10.1" "python >=3.7,<3.8.0a0"

DEFAULT_PLATFORMS = ['linux-64',
                     'linux-32',
                     'osx-64',
                     'win-64',
                     'win-32']
DEFAULT_PLATFORM = 'linux-64'
DEFAULT_CHANNEL = ['defaults']

def download(url, base_dir):
    u_path = Path('.'+ urlparse(url).path)
    p = u_path.parent
    f = u_path.name
    p = base_dir / p
    p.mkdir(parents=True, exist_ok=True)
    try:
        if (not os.path.isfile(p / f)):
            urllib.request.urlretrieve(url, p / f)
            print('Downloaded', url)
        else:
            print('Found already downloaded', url)
    except HTTPError as e:
        print(url, '-', e)

@click.command()
@click.argument('packages', nargs=-1, required=True)
@click.option('--channel', 'channels', default=DEFAULT_CHANNEL, metavar='<CHANNEL NAME>', multiple=True, help='Note: multiple --channel options are supported')
@click.option('--platform', 'platform', default=DEFAULT_PLATFORM, type=click.Choice(DEFAULT_PLATFORMS), show_default=True)
@click.option('--target-directory', 'target_dir', default='localmirror', metavar='<TARGET_DIR>', show_default=True)
def localmirror(packages, channels=None, platform=None, target_dir=None):
    base_dir = Path.cwd() / target_dir
    base_dir.mkdir(exist_ok=True)

    platforms = [platform, 'noarch']

    #defaults aka 'main' URLs
    urls = []
    defaults_base = 'https://repo.anaconda.com/pkgs/'
    paths = ['main', 'r']
    for p in paths:
        for a in platforms:
            urls.append(defaults_base + p + '/' + a + '/current_repodata.json')

    channel_base = 'https://conda.anaconda.org/'
    for c in channels:
        if (c == DEFAULT_CHANNEL[0]):
            continue
        for a in platforms:
            urls.append(channel_base + c + '/' + a + '/current_repodata.json')
            urls.append(channel_base + c + '/' + a + '/repodata.json')

    for u in urls:
        download(u, base_dir)

    if 'defaults' not in channels:
        channels = list(channels)
        channels.append('defaults')

    index = get_index(
        channel_urls=channels,
        platform=platform,
        prepend=False,
    )

    solver = Resolve(index, channels=channels)
    to_download = solver.install(packages)
    for d in to_download:
        download(d.url, base_dir)

if __name__ == "__main__":
    localmirror()
