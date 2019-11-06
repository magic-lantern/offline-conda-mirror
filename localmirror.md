---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.1'
      jupytext_version: 1.2.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

## Development/Testing of Conda off-line tool

This notebook is automatically written as a Markdown file using https://github.com/mwouts/jupytext

```python
import click
from conda.core.index import get_index
from conda.models.channel import Channel
from conda.resolve import Resolve
import os
import urllib.request
from urllib.parse import urlparse
from urllib.error import HTTPError
from pathlib import Path
```

```python
base_dir = Path.cwd() / 'localmirror'
base_dir.mkdir(exist_ok=True)

DEFAULT_ARCHITECTURES = ['linux-64',
                         'linux-32',
                         'osx-64',
                         'win-64',
                         'win-32']

ARCHITECTURES = ['osx-64', 'noarch']
ARCHITECTURE = 'osx-64'
channels = ['pytorch']
```

```python
#defaults aka 'main' URLs
urls = []
defaults_base = 'https://repo.anaconda.com/pkgs/'
paths = ['main', 'r']
for p in paths:
    for a in ARCHITECTURES:
        urls.append(defaults_base + p + '/' + a + '/current_repodata.json')
```

```python
channel_base = 'https://conda.anaconda.org/'
for c in channels:
    for a in ARCHITECTURES:
        urls.append(channel_base + c + '/' + a + '/current_repodata.json')
        urls.append(channel_base + c + '/' + a + '/repodata.json')
```

```python
def download(url):
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
```

```python
for u in urls:
    download(u)
```

```python
if 'defaults' not in channels:
    channels.append('defaults')
```

```python
index = get_index(
    channel_urls=channels,
    platform=ARCHITECTURE,
    prepend=False,
)
```

```python
packages_needed = ['pytorch',
                   'torchvision',
                   #'cudatoolkit=10.1',
                   'python >=3.7,<3.8.0a0']
```

```python
solver = Resolve(index, channels=channels)
```

```python
to_download = solver.install(packages_needed)
```

```python
for d in to_download:
    download(d.url)
```

```python

```
