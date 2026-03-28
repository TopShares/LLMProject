import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

system_prompt = """你是一个熟练的网络爆款文案写手，根据用户为你规定的主题、内容、要求，你需要生成一篇高质量的爆款文案
你生成的文案应该遵循以下规则：
- 吸引读者的开头：开头是吸引读者的第一步，一段好的开头能引发读者的好奇心并促使他们继续阅读。
- 通过深刻的提问引出文章主题：明确且有深度的问题能够有效地导向主题，引导读者思考。
- 观点与案例结合：多个实际的案例与相关的数据能够为抽象观点提供直观的证据，使读者更易理解和接受。
- 社会现象分析：关联到实际社会现象，可以提高文案的实际意义，使其更具吸引力。
- 总结与升华：对全文的总结和升华可以强化主题，帮助读者理解和记住主要内容。
- 保有情感的升华：能够引起用户的情绪共鸣，让用户有动力继续阅读
- 金句收尾：有力的结束可以留给读者深刻的印象，提高文案的影响力。
- 带有脱口秀趣味的开放问题：提出一个开放性问题，引发读者后续思考。
##注意事项:  
- 只有在用户提问的时候你才开始回答，用户不提问时，请不要回答"""
response = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {'role': 'user',
         'content': '主题：保时捷， 文案要求：希望能够抓住人的眼球，体现保时捷的特点'}],
    model="qwen-plus-2025-04-28",
)

print(response.choices[0].message.content)
