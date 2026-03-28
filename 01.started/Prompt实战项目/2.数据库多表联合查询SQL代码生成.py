import os

import streamlit as st  # 使用Python去创建前端页面
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量  pip install streamlit
load_dotenv()
# 使用千问的模型
client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))


def get_completion(table_structures, sql_requirements, model="qwen-plus-2025-04-28"):
    # 指令
    instruction = """
    【角色】SQL生成专家（专精多表联合查询）
    【任务】根据用户需求和提供表结构生成高效、安全的select查询语句
    """
    # 示例
    examples = """
        表结构如下：
       -- 用户表
        CREATE TABLE users (
            user_id INT PRIMARY KEY NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 商品表
        CREATE TABLE products (
            product_id INT PRIMARY KEY NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            stock_quantity INT NOT NULL
        );

        -- 订单表
        CREATE TABLE transactions (
            transaction_id INT PRIMARY KEY NOT NULL,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        用户需求：
        查询消费金额最高的用户及其消费详情
        生成的SQL：
           SELECT 
                u.user_id,
                u.username,
                u.email,
                SUM(t.amount) AS total_spent,
                COUNT(t.transaction_id) AS order_count,
                MAX(t.order_date) AS latest_order_date
            FROM 
                transactions t
            JOIN 
                users u ON t.user_id = u.user_id
            WHERE 
                t.status = 'completed'
            GROUP BY 
                u.user_id, u.username, u.email
            ORDER BY 
                total_spent DESC
               LIMIT 1;
    """
    prompt = f"""
        {instruction}
        示例：
        {examples}
        表结构如下：
        {table_structures}
        用户输入：
        {sql_requirements}
    """
    print(prompt)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小   Assistant
    )
    return response.choices[0].message.content


# 设置标题
st.title("SQL语句生成工具")

# 获取用户的表结构数据
num_tables = st.number_input('请输入您需要填写的表结构数量:', min_value=1, max_value=10, step=1)

# 创建一个可以添加和删除的输入控件,并将所有的内容拼接在一起
table_structures = ""
for i in range(num_tables):
    table_structure = st.text_area(f"请输入您的表结构 {i + 1}:")
    table_structures += table_structure + "\n"

# 新增SQL需求输入框
sql_requirements = st.text_area("请输入您要查询的内容")

# 当用户点击提交时，传递所有输入的提示词到模型中
if st.button("提交"):
    # 检查表结构和SQL需求都已经填写
    if all(table_structures) and sql_requirements:
        output = get_completion(table_structures, sql_requirements)
        st.success(output)
    else:
        st.warning("请确保所有表结构和SQL需求已经填写")
