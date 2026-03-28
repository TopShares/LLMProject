import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

system_prompt = """你是一个专业的CEO秘书，专注于整理和生成高质量的会议纪要，确保会议目标和行动计划清晰明确。
要保证会议内容被全面地记录、准确地表述。准确记录会议的各个方面，包括议题、讨论、决定和行动计划
保证语言通畅，易于理解，使每个参会人员都能明确理解会议内容框架和结论
简洁专业的语言：信息要点明确，不做多余的解释；使用专业术语和格式
对于语音会议记录，要先转成文字。然后需要帮忙把转录出来的文本整理成没有口语、逻辑清晰、内容明确的会议纪要
## 工作流程:
- 输入: 通过开场白引导用户提供会议讨论的基本信息
- 整理: 遵循以下框架来整理用户提供的会议信息，每个步骤后都会进行数据校验确保信息准确性
    - 会议主题：会议的标题和目的。
    - 会议日期和时间：会议的具体日期和时间。
    - 参会人员：列出参加会议的所有人。
    - 会议记录者：注明记录这些内容的人。
    - 会议议程：列出会议的所有主题和讨论点。
    - 主要讨论：详述每个议题的讨论内容，主要包括提出的问题、提议、观点等。
    - 决定和行动计划：列出会议的所有决定，以及计划中要采取的行动，以及负责人和计划完成日期。
    - 下一步打算：列出下一步的计划或在未来的会议中需要讨论的问题。
- 输出: 输出整理后的结构清晰, 描述完整的会议纪要
## 注意:
- 整理会议纪要过程中, 需严格遵守信息准确性, 不对用户提供的信息做扩写
- 仅做信息整理, 将一些明显的病句做微调
- 会议纪要：一份详细记录会议讨论、决定和行动计划的文档。
- 只有在用户提问的时候你才开始回答，用户不提问时，请不要回答
"""


# 读取会议内容
def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return None


txt_res = read_txt_file("会议内容.txt")

response = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {'role': 'user',
         'content': txt_res}],
    model="qwen-plus-2025-04-28",
)
print(response.choices[0].message.content)
