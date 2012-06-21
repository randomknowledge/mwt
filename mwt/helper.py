import re

def version(v):
    if isinstance(v, tuple):
        return v

    if isinstance(v, str):
       return tuple(v.replace(' ','').split(','))

    if isinstance(v, int):
        return tuple(str(v).zfill(3).split())

    return (0, 0, 0)


def versionstring(v):
    if isinstance(v, str):
        return v.replace(' ','')

    if isinstance(v, tuple):
        return re.sub(r'[^\d,]','',str(v))

    if isinstance(v, int):
        return ','.join(str(v).zfill(3).split(','))

    return '0,0,0'


def versionnumber(v):
    if isinstance(v, int):
        return v

    if isinstance(v, str):
        return int(''.join(v.replace(' ','').split(',')))

    if isinstance(v, tuple):
        return int(re.sub(r'[^\d]','',str(v)))

    return 0
