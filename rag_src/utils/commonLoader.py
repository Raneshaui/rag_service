import os

import yaml

def yaml_load(path) -> dict:
    """
    读取config目录下的yaml文件
    :param path:
    :return:
    """
    with open(path,'r',encoding='utf-8') as f:
        config = yaml.safe_load(f)
        return config


if __name__ == "__main__":
    print(yaml_load("J:/uvcode/rag/rag_src/config/prompt.yaml"))