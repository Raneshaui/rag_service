import os


def get_project_path():
    """
    获取项目的根目录
    :return: rag
    """
    current_path =  os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(current_path)
    project_path = os.path.dirname(parent_path)
    return project_path


def get_abstract_path(relative_path):
    """
    根据相对路径获取绝对路径
    :return:
    """
    project_path = get_project_path()
    # 构建安全的绝对路径
    abstract_path = os.path.normpath(os.path.join(project_path, relative_path))

    return abstract_path


def get_config_path():
    """
    获取config配置文件的绝对路径
    :return:
    """
    return get_abstract_path("rag_src/config")

def get_data_path():
    """
    获取数据配置的绝对路径
    :return:
    """
    return get_abstract_path("data")

def get_chathistory_path():
    """
    获取存储历史对话消息的路径
    :return:
    """
    return get_abstract_path("data/chat_history")

def get_db_path():
    """
    获取存储向量数据库的路径
    :return:
    """
    return get_abstract_path("data/chroma_db")

if __name__ == "__main__":
    print(get_project_path())
    print(f'配置目录',get_config_path())
    print(f'数据目录',get_data_path())
    print(f'历史聊天记录',get_chathistory_path())
    print(f'chmora数据库',get_db_path())