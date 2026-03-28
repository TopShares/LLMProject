# langchain_community
import os

from dotenv import load_dotenv
from langchain_community.llms.tongyi import Tongyi

# 加载环境变量
load_dotenv()

# 不用qwen3-maX，因为qwen3-max是聊天模型，qwen-max是大语言模型
model = Tongyi(model="qwen-max", api_key=os.getenv("DASHSCOPE_API_KEY"))
res = model.invoke(input='你是谁？能做什么？')
print(res)
