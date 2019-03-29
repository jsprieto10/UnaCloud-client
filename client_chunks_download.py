import requests
import os
from helper import join
import time


def get_routes(local_filename):
    url = 'http://localhost:8000/routes/{}'.format(local_filename)
    r=requests.get(url)
    return r.json()['data']


def download_file(url,fol,local_filename):
    # NOTE the stream=True parameter below
    
    fil = os.path.join(fol,local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fil, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return fil

def create_dir_or_clear(dest):
    dest_folder = os.path.join('download', 'chunks',dest)
    if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
    else:
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))
    return dest_folder


start = time.time()

name = 'test.mp4'
names_routes = 'split-{}'.format(name)
file_name = 'join-{}'.format(name)

chunks = get_routes(names_routes)

folder = create_dir_or_clear(names_routes)

chunk_size = 256*1024

for chunk in chunks:
    url = 'http://localhost:8000/download/{}'.format(names_routes+'-'+chunk)
    download_file(url,folder,chunk)


dest = dest_folder = os.path.join('download', 'chunks',name)


join(folder,dest,chunk_size)

end = time.time()
print(end-start)