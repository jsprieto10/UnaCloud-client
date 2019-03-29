import requests
import time
import os


def download_file(url,local_filename):
    # NOTE the stream=True parameter below
    fil = os.path.join('download', 'normal',local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fil, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return fil

start = time.time()

file_name = 'join-test.mp4'
url = 'http://localhost:8000/download/{}'.format(file_name)


download_file(url,file_name)

end = time.time()

print(end-start)