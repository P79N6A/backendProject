import ctypes
import commands
import json
import hashlib

ffprobe_path = 'ffprobe'
ffprobe_args = '-timeout 8000 -v quiet -print_format json -show_streams -select_streams v -i %s'

def tobytes(data, buf_len, encoding=''):
    """Convert a BitArray instance to a ctypes byte array instance"""
    if encoding:
        buf = bytearray(data, encoding)
    else:
        buf = bytearray(data)
    buffer = (ctypes.c_byte * buf_len).from_buffer(buf)
    return buffer

def toubytes(data, buf_len):
    """Convert a BitArray instance to a ctypes byte array instance"""
    buf = bytearray(data)
    buffer = (ctypes.c_ubyte * buf_len).from_buffer(buf)
    return buffer

def toubyte(data):
    """Convert a BitArray instance to a ctypes byte array instance"""
    buf = bytearray(data)
    buffer = (ctypes.c_ubyte).from_buffer(buf)
    return buffer

def md5_str(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5_bin(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def sha_str(fname):
    hash_sha = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha.update(chunk)
    return hash_sha.hexdigest()

def sha_bin(fname):
    hash_sha = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha.update(chunk)
    return hash_sha.digest()

def get_video_meta_info(v_url):
    cmd = '%s %s' % (ffprobe_path, ffprobe_args % v_url)
    status,output = commands.getstatusoutput(cmd)
    data = json.loads(output)
    if data.has_key('streams'):
        video_streams = data['streams']
        if len(video_streams):
            video_stream = video_streams[0]
            return video_stream
    return None


if __name__ == "__main__":
    file_path = '/Users/shawn/demo/tmp/video/8f137c87-2fd3-11e8-9615-6c4008a99b3a/67a95fef208949a5bdc7adfaadcc480b.mp4'
    print len(sha_bin(file_path))
    print len(sha_str(file_path))
    print len(md5_bin(file_path))
    print len(md5_str(file_path))
