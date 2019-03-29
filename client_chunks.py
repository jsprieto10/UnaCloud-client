import requests
import os
from helper import join
import time


def get_routes(local_filename):
    url = 'http://localhost:8000/routes/{}'.format(local_filename)
    r=requests.get(url)
    return r.json()['data']


start = time.time()

name = 'test.mp4'

names_routes = 'split-{}'.format(name)

chunks = get_routes(names_routes)

chunk_size = 256*1024
source = names_routes

fil = os.path.join('download', 'chunkie',name)

output_file = open(fil, 'wb')


for c in chunks:
    url = 'http://localhost:8000/download/{}'.format(names_routes+'-'+c)
    # NOTE the stream=True parameter below

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    output_file.write(chunk)
                    # f.flush()

output_file.close()


end = time.time()

print(end-start)