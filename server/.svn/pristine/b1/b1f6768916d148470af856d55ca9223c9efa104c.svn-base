# -*- coding: UTF-8 -*-
import ConfigParser

def read_server_config(filename='cfg/conf.cfg', section='server'):
    conf = read_config(filename, section)
    conf['port'] = int(conf['port'])
    return conf


def read_db_config(filename='cfg/conf.cfg', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    conf = read_config(filename, section)
    conf['port'] = int(conf['port'])
    return conf

def read_link_domain(filename='cfg/conf.cfg', section='link'):
    conf = read_config(filename, section)
    domain = conf['domain']
    return domain

def read_l5_info(filename='cfg/conf.cfg', section='l5'):
    conf  = read_config(filename, section)
    modid = conf['modid']
    cmdid = conf['cmdid']

    return (modid, cmdid)


def _read_video_url_config(filename='cfg/conf.cfg', section='url',  ext='mp4',
                           v=None):
    url = ''
    if int(v.src_type) == 0:
        conf = read_config(filename, section)
        definition = str(v.definition) + 'P'
        url =  conf['video'] % ('%s.%s' % (v.video_id,ext), definition, v.version)
    elif int(v.src_type) == 1:
        url = v.url + '&definition=%sP'% v.definition
    elif int(v.src_type) == 2:
        url = v.url + '&definition=%sP'% v.definition

    return url

def _read_cover_url_config(filename='cfg/conf.cfg', section='url',  v=None,
                           ext='jpg'):
    url = ''
    if int(v.src_type) == 0:
        conf = read_config(filename, section)
        url =  conf['cover'] % '%s.%s' % (v.video_id,ext)
    elif int(v.src_type) == 1:
        url = v.cover
    elif int(v.src_type) == 2:
        url = v.cover

    return url

def _read_icon_url_config(filename='cfg/conf.cfg', section='url',  cid='',
                           ext='png'):
    conf = read_config(filename, section)
    url =  conf['icon'] % '%s.%s' % (cid,ext)
    return url

def _read_music_url_config(filename='cfg/conf.cfg', section='url',  ext='mp3',
                           m=None):
    url = ''
    conf = read_config(filename, section)
    if not m:
        m = 'test'
    url =  conf['music'] % '%s.%s' % (m, ext)
    return url

def read_icon_url_config(c):
    #if len(c) and c[len(c) - 1] == '2':
    #    c = '推荐2'
    #else:
    #    c = '推荐'
    return _read_icon_url_config(cid=c)

def read_icon_url_f_config(c):
    #if len(c) and c[len(c) - 1] == '2':
    #    c = '推荐2'
    #else:
    #    c = '推荐'
    return _read_icon_url_config(cid=c+'_focus')

def read_icon_url_s_config(c):
    #if len(c) and c[len(c) - 1] == '2':
    #    c = '推荐2'
    #else:
    #    c = '推荐'
    return _read_icon_url_config(cid=c+'_select')

def read_cover_url_config(v):
    return _read_cover_url_config(v=v)

def read_video_url_config(v):
    return _read_video_url_config(v=v)

def read_music_url_config(m):
    return _read_music_url_config(m=m)

def read_log_path_config(filename='cfg/conf.cfg', section='log', logname=''):
    if logname:
        conf = read_config(filename, section)
        path = conf['path'] % logname
        return path
    else:
        raise Exception('need logname')

def read_config(filename, section):
    parser = ConfigParser.ConfigParser()
    parser.read(filename)

    if not filename or not section:
        raise Exception('need filename and section')
        return

    # get section, default to mysql
    dic = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            dic[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return dic

if __name__ == "__main__":
    print read_db_config()
