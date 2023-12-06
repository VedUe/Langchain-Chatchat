from langchain.document_loaders import TextLoader

path = "./knowledge_base/gems/content/08-相似宝石鉴定特征单晶-多晶（GIC证书）.md"
loader = TextLoader
content = loader(path).load()
print(content)

