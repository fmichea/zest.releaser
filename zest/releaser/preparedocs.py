from __future__ import unicode_literals

import os

from zest.releaser import addchangelogentry
from zest.releaser import prerelease
from zest.releaser import release
from zest.releaser import postrelease
from zest.releaser.utils import read_text_file
from zest.releaser.utils import write_text_file


def prepare_entrypoint_documentation(data):
    """Place the generated entrypoint doc in the source structure."""
    if data['name'] != 'zest.releaser':
        # We're available everywhere, but we're only intended for
        # zest.releaser internal usage.
        return
    target = os.path.join(data['reporoot'], 'doc', 'source',
                          'entrypoints.rst')
    marker = '.. ### AUTOGENERATED FROM HERE ###'
    result = []
    lines, encoding = read_text_file(target)
    for line in lines.split('\n'):
        line = line.rstrip()
        if line == marker:
            break
        result.append(line)
    result.append(marker)
    result.append('')

    for name, datadict in (
            ('prerelease', prerelease.DATA),
            ('release', release.DATA),
            ('postrelease', postrelease.DATA),
            ('addchangelogentry', addchangelogentry.DATA),
            ):
        heading = '%s data dict items' % name.capitalize()
        result.append(heading)
        result.append('-' * len(heading))
        result.append('')
        for key in sorted(datadict.keys()):
            result.append(key)
            result.append('    ' + datadict[key])
            result.append('')

    write_text_file(target, '\n'.join(result), encoding)
    print("Wrote entry point documentation to %s" % target)
