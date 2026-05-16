from watchdog.watchmedo import load_config
from rag_src.utils.commonLoader import yaml_load
from rag_src.utils.pathTool import get_abstract_path
rag_prompt = yaml_load(get_abstract_path("rag_src/config/prompt.yaml"))




if __name__ == "__main__":
    print(rag_prompt)
    print(rag_prompt.get('rag_prompt','rag_prompt'))



