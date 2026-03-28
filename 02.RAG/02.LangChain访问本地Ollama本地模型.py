# langchain_community

from langchain_ollama import OllamaLLM

# 不用qwen3-maX，因为qwen3-max是聊天模型，qwen-max是大语言模型
model = OllamaLLM(model="qwen3:4b")
res = model.invoke(input='你是谁？能做什么？')
print(res)
