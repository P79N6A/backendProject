import ConfigParser

def read_appid():
    return 'wx3566ceb82d2e0f2d'

def read_db_config(filename='cfg/conf.cfg', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    conf = read_config(filename, section)
    conf['port'] = int(conf['port'])
    return conf

def read_path_config(filename='cfg/conf.cfg', section='path', pathname=''):
    if pathname:
        conf = read_config(filename, section)
        path = conf[pathname]
        return path
    else:
        raise Exception('need pathname')


def read_log_path_config(filename='cfg/conf.cfg', section='log', logname=''):
    if logname:
        conf = read_config(filename, section)
        path = conf['path'] % logname
        return path
    else:
        raise Exception('need logname')

def read_l5_info(filename='cfg/conf.cfg', section='l5'):
    conf  = read_config(filename, section)
    modid = conf['modid']
    cmdid = conf['cmdid']

    return (modid, cmdid)

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
