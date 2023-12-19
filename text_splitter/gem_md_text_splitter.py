from langchain.text_splitter import CharacterTextSplitter
import re
from typing import List
import sys
sys.path.append('/code/Langchain-Chatchat')
from configs.kb_config import CHUNK_SIZE, OVERLAP_SIZE

class GemTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = 600, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:
        if self.pdf:
            text = re.match(r"\n{3,}", "\n", text)
            text = re.match('\s', ' ', text)
            text = text.replace("\n\n", "")
        sent_sep_pattern = re.compile(r'\n')
        sent_list0 = []
        for ele in sent_sep_pattern.split(text):
            if sent_sep_pattern.match(ele) and sent_list0:
                sent_list0[-1] += ele
            elif ele:
                sent_list0.append(ele)       
        return sent_list0
    
if __name__ == "__main__":
    with open('/code/Langchain-Chatchat/knowledge_base/gems/content/heads.txt', 'r', encoding='utf-8') as fr:
        text = fr.read()
    text_splitter = GemTextSplitter()
    sent_list = text_splitter.split_text(text)
    for i in range(10, 20):
        print(sent_list[i] + '\n===')
