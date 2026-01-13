# chatglm3_official.py - ChatGLM3官方推理代码（完整版）
# -*- coding: utf-8 -*-
import os
import torch
from transformers import AutoTokenizer, AutoModel

# ========== 核心：指向你的本地ChatGLM3-2B模型路径 ==========
MODEL_PATH = "D:/cooker/chatglm3-2b"

# 适配你的GTX 1650 Ti（4GB显存）
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
torch.cuda.empty_cache()

def main():
    print("===== ChatGLM3-2B 官方交互式对话 =====")
    print("📌 模型路径：", MODEL_PATH)
    print("📌 运行设备：", "GPU (CUDA)" if torch.cuda.is_available() else "CPU")
    print("💡 输入 'clear' 清空对话历史 | 输入 'stop' 退出程序\n")

    # 加载模型和分词器（trust_remote_code=True是关键）
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        model = AutoModel.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16,  # 半精度，节省显存
            device_map="auto",          # 自动分配到GPU/CPU
            trust_remote_code=True
        ).eval()  # 推理模式，禁用训练
    except Exception as e:
        print(f"❌ 模型加载失败：{type(e).__name__}: {str(e)[:200]}")
        print("💡 请确认：1.模型文件完整 2.已安装依赖 accelerate/sentencepiece")
        return

    # 对话历史初始化
    history = []
    while True:
        # 获取用户输入
        user_input = input("你：").strip()
        if not user_input:
            continue
        
        # 退出/清空逻辑
        if user_input.lower() == "stop":
            print("ChatGLM3：再见～👋")
            break
        if user_input.lower() == "clear":
            history = []
            print("ChatGLM3：对话历史已清空～😜")
            continue
        
        # 核心：调用模型生成回复（带上下文记忆）
        response, history = model.chat(
            tokenizer,
            user_input,
            history=history,
            max_length=2048,
            temperature=0.7,
            top_p=0.85
        )
        
        # 打印回复
        print(f"ChatGLM3：{response}\n")

if __name__ == "__main__":
    main()