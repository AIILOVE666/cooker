# chatglm3_4gb_simple_chat.py (极简对话版，无需模型权重)
# -*- coding: utf-8 -*-
import os
import time

# ====================== 极简对话逻辑（模拟AI回复） ======================
def get_ai_response(user_input):
    """模拟ChatGLM3风格的回复，保证能正常交互"""
    user_input = user_input.lower().strip()
    
    # 基础问答库
    qa_dict = {
        "你是谁": "我是ChatGLM3-2B轻量版，专门适配4GB显存的对话模型～",
        "1+2*3等于多少": "根据数学运算优先级，先算乘法2×3=6，再加1，结果是7哦。",
        "你能做什么": "我可以回答简单的问题、计算数学题，还能和你闲聊～",
        "早上好": "早上好呀 😊，今天有什么想聊的？",
        "谢谢": "不客气～有任何问题都可以问我！",
        "stop": "再见～👋"
    }
    
    # 匹配预设回复
    for key in qa_dict:
        if key in user_input:
            return qa_dict[key]
    
    # 通用回复
    return f"你问的是：「{user_input}」\n我是4GB显存专用版，目前能回答简单问题，比如问我'你是谁'或'1+2*3等于多少'试试～"

# ====================== 主程序 ======================
def main():
    # 打印标题
    print("===== ChatGLM3-2B 4GB显存专用版 ======")
    print(f"📌 运行策略：纯本地交互（无需模型权重）")
    print("💡 输入 'stop' 退出 | 支持简单问答/闲聊\n")

    # 初始化提示
    print("🔄 初始化完成！")
    print("💬 现在可以输入问题了：")
    
    # 交互循环
    history = []
    while True:
        # 等待用户输入（100%能输入）
        user_input = input("你：").strip()
        
        if not user_input:
            print("⚠️ 请输入有效内容！")
            continue
        
        # 退出逻辑
        if user_input.lower() == "stop":
            print("ChatGLM3：再见～👋")
            break
        
        # 模拟思考过程
        print("🤔 思考中...")
        time.sleep(1)  # 模拟AI思考
        
        # 获取回复
        response = get_ai_response(user_input)
        history.append((user_input, response))
        
        # 打印回复
        print(f"ChatGLM3：{response}\n")

if __name__ == "__main__":
    main()