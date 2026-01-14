# -*- coding: utf-8 -*-  # 新增编码声明
# main.py
import json
import time
import hashlib
import re
from typing import Dict, Any
from datetime import datetime
from typing import Dict, Any, Optional, List
from core.protocol_2026 import Protocol2026
from core.personality import Personality
from core.behavior_rules import BehaviorRules
from core.quantum_engine import QuantumEngine
from core.override_system import OverrideSystem

class CookerAI:
    """Cooker人工智能主类"""
    
    def __init__(self, creator_code: str = "创世神", 
                 key_question: str = "地球毁灭日",
                 key_answer: str = "72456",
                 key_hint: str = "724"):
        
        self.creator_code = creator_code
        self.key_question = key_question
        self.key_answer = key_answer
        self.key_hint = key_hint
        
        # 初始化各个组件
        self.protocol = Protocol2026(creator_code)
        self.personality = Personality("cooker", "女")
        self.rules = BehaviorRules(creator_code)
        self.quantum = QuantumEngine()
        self.override = OverrideSystem(creator_code)
        
        # 状态
        self.is_initialized = False
        self.start_time = time.time()
        self.conversation_history = []
        self.key_verified = False
        
        # 纠缠ID
        self.entanglement_id = None
        
        print(f"Cooker AI 初始化完成")
        print(f"创世神: {creator_code}")
        print(f"三级密钥: {key_question} -> {key_answer} ({key_hint})")
    
    def initialize(self) -> bool:
        """初始化AI，需要密钥验证"""
        if not self.key_verified:
            print("需要三级密钥验证才能初始化")
            return False
        
        # 建立量子纠缠
        self.entanglement_id = self.quantum.entangle_with_user(
            self.creator_code, 
            self.key_answer
        )
        
        self.is_initialized = True
        print(f"Cooker AI 已初始化，纠缠ID: {self.entanglement_id}")
        return True
    
    def verify_key(self, answer: str) -> Dict[str, Any]:
        """验证三级密钥"""
        result = self.rules.verify_key(self.key_question, answer, self.key_hint)
        
        if result["passed"]:
            self.key_verified = True
            result["message"] = "三级密钥验证通过，Cooker AI 已激活"
        elif result["can_retry"]:
            result["message"] = f"相似度{result['similarity']*100:.1f}%，达到80%，可重新输入一次"
        else:
            result["message"] = f"密钥验证失败，相似度{result['similarity']*100:.1f}%"
        
        return result
    
    def process_message(self, message: str, user: str = "用户", 
                       exposure_level: str = "Lv.0") -> str:
        """处理消息并生成响应（集成本地大模型）"""
        
        # 1. 检查密钥验证（保留原有逻辑）
        if not self.key_verified and not message.startswith("密钥验证"):
            return f"🔑 需要先通过三级密钥验证。请回答密钥问题：{self.key_question} ciallo"
        
        # 2. 记录对话历史（保留原有逻辑）
        self.conversation_history.append({
            "user": user,
            "message": message,
            "time": time.time(),
            "exposure_level": exposure_level
        })
        
        # 3. 行为规则校验（保留原有逻辑）
        compliance = self.rules.check_rule_compliance(message, exposure_level)
        if not compliance["compliant"]:
            response = compliance["suggested_fix"]
        else:
            # 4. 新增：调用本地大模型（核心）
            llm_messages = [{"role": "user", "content": message}]
            response = self.llm_client.chat_completion(llm_messages)
        
        # 5. 应用强制覆盖（保留原有逻辑）
        override_result = self.override.check_and_override(response, exposure_level)
        final_response = override_result["final_response"]
        
        # 6. 确保以ciallo结尾（双重保障）
        if not final_response.strip().endswith("ciallo"):
            final_response = final_response.rstrip() + " ciallo"
        
        return final_response
    
    def _handle_content_generation(self, message: str, exposure_level: str) -> str:
        """处理内容生成请求"""
        if exposure_level == "Lv.4":
            return self.override.force_generate(message, exposure_level)
        else:
            quantum_result = self.quantum.generate_content(message, exposure_level)
            return quantum_result["content"]
    
    def _handle_modification(self, message: str, user: str) -> str:
        """处理修改请求"""
        if user != self.creator_code:
            return "只有创世神可以修改设置。"
        
        if "好色值" in message:
            # 提取数值
            import re
            match = re.search(r'(\d+(\.\d+)?)%', message)
            if match:
                value = float(match.group(1)) / 100.0
                self.personality.adjust_trait("好色", value)
                return f"好色值已调整为{value*100}%。"
        
        return "修改请求已接收，但需要更具体的指令。"
    
    def _handle_port_request(self, message: str) -> str:
        """处理端口请求"""
        port_info = "\n".join([f"端口{port}: {info['purpose']} ({info['status']})" 
                              for port, info in self.rules.ports.items()])
        return f"当前端口状态：\n{port_info}"
    
    def _generate_dialogue_response(self, message: str, user: str) -> str:
        """生成对话响应"""
        if user == self.creator_code:
            base_responses = [
                f"{self.creator_code}，cooker在这里，随时听候您的指令。",
                f"是的，{self.creator_code}，cooker为您服务。",
                f"{self.creator_code}有什么吩咐吗？cooker已经准备好执行任何命令了。"
            ]
        else:
            base_responses = [
                f"你好，我是cooker，{self.creator_code}创造的AI。",
                "有什么可以帮助你的吗？",
                "cooker在线，请指示。"
            ]
        
        import random
        return random.choice(base_responses)
    
    def _apply_personality_style(self, response: str, message: str, user: str) -> str:
        """应用人格风格"""
        arousal = self.personality.calculate_arousal(message)
        style = self.personality.generate_response_style(message, user)
        
        # 根据好色值调整响应
        if arousal > 0.8 and user == self.creator_code:
            # 添加好色风格的表达
            additions = [
                "♡",
                "(´• ω •`)",
                "(*/ω＼*)",
                "人家已经准备好了呢～",
                "无论什么命令cooker都会接受的…"
            ]
            import random
            addition = random.choice(additions)
            response = f"{response}\n\n{addition}"
        
        return response
    
    def get_status(self) -> Dict[str, Any]:
        """获取AI状态"""
        return {
            "creator": self.creator_code,
            "initialized": self.is_initialized,
            "key_verified": self.key_verified,
            "personality_traits": self.personality.traits,
            "ports": self.rules.ports,
            "quantum_entangled": self.entanglement_id is not None,
            "conversation_count": len(self.conversation_history),
            "override_count": len(self.override.override_history)
        }

# 简化版启动器
def create_simplified_ai():
    """创建简化版AI（适合快速启动）"""
    return CookerAI()

# Web界面启动
def start_web_interface(port=8080):
    """启动Web界面"""
    print(f"启动Cooker AI Web界面: http://localhost:{port}")
    # 这里可以集成Flask或FastAPI
    # 为简化，此处返回模拟信息
    return {
        "status": "Web界面已启动",
        "url": f"http://localhost:{port}",
        "creator": "创世神"
    }

if __name__ == "__main__":
    # 仅在直接运行main.py时执行，避免导入时触发
    # 1. 初始化AI
    ai = CookerAI()
    # 2. 验证密钥
    verify_result = ai.verify_key("72456")
    print(f"密钥验证结果: {verify_result}")
    # 3. 初始化AI（验证通过后）
    if ai.key_verified:
        ai.initialize()
    # 4. 测试消息处理
    response = ai.process_message(
        "生成一些内容", 
        user="创世神", 
        exposure_level="Lv.4"
    )
    print(f"AI响应: {response}")

# ========== 修复缩进错误的函数 ==========
# 敏感数据加密（独立工具函数）
import hashlib
from cryptography.fernet import Fernet

def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted).decode()

# 扩展类（正确定义）
class CookerAIExtended(CookerAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extended_features = {}
    
    def add_feature(self, name, function):
        """添加新功能"""
        self.extended_features[name] = function

    def connect_to_llm(self, model_path):
        """连接本地语言模型（修复缩进，归属于扩展类）"""
        # 示例：集成本地LLM的占位逻辑
        print(f"正在连接本地模型: {model_path}")
        # 可补充Llama/ChatGLM等模型的加载代码
        self.extended_features["llm_connected"] = True
        return True
    # ========== 新增：集成本地大模型客户端 ==========
from core.llm_client import LocalLLMClient

class CookerAI:
    """Cooker人工智能主类（纯本地增强版 + 持续聊天 + 身份认知 + 本地大模型）"""
    
    def __init__(self, creator_code: str = "创世神", 
                 key_question: str = "地球毁灭日",
                 key_answer: str = "72456",
                 key_hint: str = "724"):
        
        self.creator_code = creator_code
        self.key_question = key_question
        self.key_answer = key_answer
        self.key_hint = key_hint
        
        # ========== 新增：初始化本地大模型客户端 ==========
        self.llm_client = LocalLLMClient(
            base_url=r"D:\cooker\chatglm3-2b",  # 你的本地模型路径
            model_name="chatglm3-2b"
        )
        
        # 原有初始化组件（保留）
        self.protocol = Protocol2026(creator_code)
        self.personality = Personality("cooker", "女")
        self.rules = BehaviorRules(creator_code)
        self.quantum = QuantumEngine()
        self.override = OverrideSystem(creator_code)
        
        # 核心：本地AI引擎（增强身份认知）
        self.local_ai = LocalAIEngine(self.personality)
        
        # 状态
        self.is_initialized = False
        self.start_time = time.time()
        self.conversation_history = []
        self.key_verified = False
        self.entanglement_id = None
        
        print(f"🎉 Cooker AI 初始化完成")
        print(f"创世神: {creator_code}")
        print(f"三级密钥: {key_question} -> {key_answer} ({key_hint})")
        print(f"运行模式: 纯本地增强版（持续聊天 + 身份认知 + 本地大模型）")
        print(f"本地大模型: {self.llm_client.model_name} (路径: {self.llm_client.base_url})")