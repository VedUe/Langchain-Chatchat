from langchain.text_splitter import CharacterTextSplitter
import re
from typing import List
import sys
sys.path.append('/code/Langchain-Chatchat')
from configs.kb_config import CHUNK_SIZE, OVERLAP_SIZE

MIN_SIZE = 100

def is_only_title(text):
    if len(text.split('\n\n')) == 1:
        return True
    return False

def get_hc(sent, h, c):
    if is_only_title(sent):
        h = sent
        c = ''
    else:
        h = re.split(r'\n+', sent)[0]
        c = sent[len(h + '\n\n'):]
    return h, c


class GemTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = 250, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:   ##此处需要进一步优化逻辑
        if self.pdf:
            text = re.match(r"\n{3,}", "\n", text)
            text = re.match('\s', ' ', text)
            text = text.replace("\n\n", "")
        sent_sep_pattern = re.compile(r'\n(?=#{1,3} )')
        sent_list0 = []
        for ele in sent_sep_pattern.split(text):
            if sent_sep_pattern.match(ele) and sent_list0:
                sent_list0[-1] += ele
            elif ele:
                sent_list0.append(ele)
        sent_list1 = []
        h1 = ''
        h2 = ''
        h3 = ''
        new_doc_parts = []
        for sent in sent_list0:
            part_list = re.split(r'\n+', sent) 
            for part in part_list:
                new_doc_parts.append(part)
                new_doc = '\n\n'.join(new_doc_parts)
                if len(new_doc) >= MIN_SIZE and len(new_doc) <= CHUNK_SIZE:
                    sent_list1.append(new_doc)
                    new_doc_parts = []
                if len(new_doc) > CHUNK_SIZE:
                    pass
            if re.match(r'^# .+', sent):
                h1, c1 = get_hc(sent, h1, c1)
            elif re.match(r'^## .+', sent):
                h2, c2 = get_hc(sent, h2, c2)
            elif re.match(r'^### .+', sent):
                h3, c3 = get_hc(sent, h3, c3)
            h = f'# {h1}\n##{h2}\n###{h3}'
            
                    

if __name__ == '__main__':
    text = open('./珠宝知识库/content/07-贵重宝石（GIC证书）.md').read()
    text_splitter = GemTextSplitter()
    sent_list = text_splitter.split_text(text)
    for i in range(10):
        print(sent_list[i])
        
