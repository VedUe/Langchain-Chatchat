import json
import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig

model_path = "/code/LLMs/baichuan-13B-chat-int4"
tokenizer = AutoTokenizer.from_pretrained(
    model_path, use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained(model_path)

fh = open('mysql/source/idx2head.json', 'r', encoding='utf-8')
fc = open('mysql/source/idx2content.json', 'r', encoding='utf-8')

jh = json.load(fh)
jc = json.load(fc)

fh.close()
fc.close()

fw = open('mysql/output/idx2head.json', 'a', encoding='utf-8')
tmp_lst = []
for idx in range(12134, len(jh)):
    j = {}
    j['idx'] = idx
    h = jh[idx]['head']
    c = jc[idx]['content']
    prompt = f'以下是一段文本```标题：{h}\n\n内容：{c}```\n\n根据原标题和内容总结一个新标题以及若干个检索用关键词'
    messages = [{"role": "user", "content": prompt}]
    response = model.chat(tokenizer, messages)
    j['head'] = response
    print(f'[idx:{idx} - {response}]')
    fw.write(str(json.dumps(j, ensure_ascii=False)) + '\n')
