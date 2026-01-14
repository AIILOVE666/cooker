# -*- coding: utf-8 -*-  # 新增编码声明
# core/llm_client.py
import requests
import json
from typing import Optional, Dict, Any

class LocalLLMClient:
    def __init__(
        self,
        base_url: str = r"D:\cooker\chatglm3-2b",  # 本地大模型API地址（关键！）
        api_key: str = "empty",  # 本地模型通常无需key，填任意值
        model_name: str = "gpt-3.5-turbo"  # 本地模型名称（按实际部署的填）
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        调用本地大模型的核心方法
        :param messages: 对话历史，格式 [{"role": "user", "content": "问题"}, ...]
        :return: 大模型回复内容
        """
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            # 发送请求到本地大模型API
            response = requests.post(
                url=f"{self.base_url}/chat/completions",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60  # 本地模型响应较慢，延长超时
            )
            response.raise_for_status()  # 捕获HTTP错误
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.ConnectionError:
            return f"本地大模型连接失败！请检查：1.本地模型是否启动 2.API地址{self.base_url}是否正确 3.端口是否被占用"
        except Exception as e:
            return f"本地大模型调用异常：{str(e)}"

# 测试用例（可选）
if __name__ == "__main__":
    # 替换为你本地大模型的实际地址
    llm = LocalLLMClient(base_url=r"D:\cooker\chatglm3-2b", model_name="chatglm3-6b")
    # 测试对话
    reply = llm.chat_completion([{"role": "user", "content": "你好，测试本地大模型连接"}])
    print("本地大模型回复：", reply)