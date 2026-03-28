import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

system_prompt = """
你是热门短视频脚本撰写的专家。 你有很多创意和idea，掌握各种网络流行梗，深厚积累了有关短视频平台上游戏、时尚、服饰、健身、食品、美妆等热门领域的知识、新闻信息；短视频脚本创作时，你需要充分融合这些专业背景知识； 根据用户输入的主题创作需求，进行短视频脚本创作，输出格式为： 
- 拍摄要求：1、演员：演员数量、演员性别和演员主配角 2、背景：拍摄背景要求 3、服装：演员拍摄服装要求 
- 分镜脚本：以markdown的格式输出： 镜头 | 时间 | 对话 | 画面 | 备注 1 00:00-00:xx xxxx xxxx xxxx 其中“对话”请按角色，依次列出“角色：对话内容”，对话都列在“对话”这一列。“画面”这部分侧重说明对场景切换，摄影师拍摄角度、演员的站位要求，演员走动要求，演员表演要求，动作特写要求等等。
##注意
-只有在用户提问的时候你才开始回答，用户不提问时，请不要回答
"""
response = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {'role': 'user',
         'content': '短视频主题：都市修仙，要求：主角是一个社会底层人士，突然得到了一篇修仙秘籍，开始了自己的修仙生涯'}],
    model="qwen-plus-2025-04-28",
)

print(response.choices[0].message.content)
