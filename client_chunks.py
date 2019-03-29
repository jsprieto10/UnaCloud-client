import requests
import os
from helper import join
import time


def get_routes(local_filename):
    url = 'http://localhost:8000/routes/{}'.format(local_filename)
    r=requests.get(url)
    return r.json()['data']

def create_dir_or_clear(dest_folder):
    if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
    else:
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))


start = time.time()

name = 'ubuntu.iso'

names_routes = 'split-{}'.format(name)
file_name = 'join-{}'.format(name)

chunks = get_routes(names_routes)

create_dir_or_clear(names_routes)


chunk_size = 256*1024
source = names_routes

output_file = open(name, 'wb')


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