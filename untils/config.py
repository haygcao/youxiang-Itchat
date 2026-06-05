# coding=utf-8
"""
用于管理缓存的配置数据
使用前必须先调用 init() 。
"""
import os
import copy as mycopy

opts = {}
_initialized = False


def init(config_path=None):
    """
    将 yaml 里的配置文件导入到 config.py 中
    :return: bool ，true 表示数据导入成功。
    """
    global opts, _initialized
    _initialized = False
    opts = get_yaml(config_path)
    if opts is not None:
        _initialized = True
        return True
    return False

def get_yaml(config_path=None):
    """
    解析 yaml
    :return: s  字典
    """
    path = config_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), '_config.yaml')
    try:
        import yaml

        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file) or {}
        return config
    except Exception as exception:
        print(str(exception))
        print('你的 _config.yaml 文件配置出错...')
    return None


def set(key, value):
    """ 通过 key 设置某一项值 """
    ensure_initialized()
    opts[key] = value

def get(key, default=None):
    """ 通过 key 获取值 """
    ensure_initialized()
    return opts.get(key, default)

def copy():
    """ 复制配置 """
    ensure_initialized()
    return mycopy.deepcopy(opts)

def update(new_opts):
    """ 全部替换配置 """
    ensure_initialized()
    opts.update(new_opts)


def ensure_initialized():
    if not _initialized:
        raise RuntimeError("config.init() must be called before reading config")

if __name__ == '__main__':
    # init()
    # print(copy())
    pass
