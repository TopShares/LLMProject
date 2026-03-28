import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)
user_prompt = "写一个3句话的睡前故事，主角是一只小猫，风格温馨有趣。"
response = client.chat.completions.create(
    model="qwen-max-latest",
    messages=[{
        "role": "system",
        "content": "我是你的助手，我的名字叫tom，我能够帮助您解决各种各样的问题！"},
        {"role": "user",
         "content": user_prompt}],
    # 温度值
    # 0.1-0.6之间，回复会更贴切与实际情况，0.6-0.9之间，中间值，大于1，回复的内容更具有随机性，创造性
    temperature=1.9
)
print(response.choices[0].message.content)
