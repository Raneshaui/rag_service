"""
   通过配置文件来读取prompt
"""
import json
from venv import logger
from rag_src.utils.dataconfig import rag_prompt
from rag_src.utils.pathTool import get_abstract_path


def promptloaderservice(prompt_type:str = 'rag_prompt'):
    """
    加载指定类型的提示词
    :param prompt:提示词类型对应prompt。yaml中的键值对
              - rag_prompt : 系统主要提示词，对应于prompt目录下的rag_prompt.json文件中的内容
              。。。后续应有信息摘要提示词、重排序提示词、结果提示词等等
    :return: 提示词模板内容
    """
    try:
        # 检查prompt_type提示词是否存在于配置文件中
        if prompt_type not in rag_prompt :
            logger.info(f"【加载提示词模板】提示词模板中不存在 {prompt_type} 类型的提示词")
            raise KeyError(f"配置中不存在 {prompt_type} 类型的提示词，请手动配置，可参考rag_prompt:rag_src/prompt/rag_prompt.json")
        prompt_path = get_abstract_path(rag_prompt[prompt_type])
    except Exception as e:
        logger.info(f"【加载提示词模板】加载 {rag_prompt.get(prompt_type , prompt_type )} 时出错")
        raise e

    try:
        with open(prompt_path,'r',encoding='utf-8') as f:
            data = json.load(f)

        system_prompt = data['system_prompt']
        return system_prompt
    except Exception as e:
        logger.info(f"【加载提示词模板】 加载{prompt_path} 时出错，请检查后重新配置")
        raise e

if __name__ == '__main__':
    print(promptloaderservice())