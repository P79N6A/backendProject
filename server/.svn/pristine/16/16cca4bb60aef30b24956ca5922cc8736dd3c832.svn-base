import ConfigParser


def init_sng_voice_config(filename = 'cfg/conf.cfg', section = 'sng_voice_interface'):
    conf = read_config(filename, section)
    
    conf['appid']     = int(conf['appid'])
    conf['projectid'] = int(conf['projectid'])
    
    return conf

def read_config(filename = None, section = None):
    dic = {}

    if (filename is None or section is None):
        raise Exception('need filename and section')

    # 防止空串    
    if (not filename or not section):
        raise Exception('need filename and section')

    parser = ConfigParser.ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            dic[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return dic

