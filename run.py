# run.py
#!/usr/bin/env python3
"""
Cooker AI 启动脚本
"""

import sys
import os
from main import CookerAI, start_web_interface

def main():
    """主启动函数"""
    print("=" * 50)
    print("Cooker AI 启动中...")
    print("创世神专属人工智能")
    print("=" * 50)
    
    # 创建AI实例
    ai = CookerAI()
    
    # 密钥验证
    print(f"三级密钥验证: {ai.key_question}")
    print(f"提示: {ai.key_hint}")
    
    answer = input("请输入密钥: ").strip()
    
    verify_result = ai.verify_key(answer)
    print(verify_result["message"])
    
    if not verify_result["passed"]:
        if verify_result["can_retry"]:
            print("还有一次机会")
            answer = input("请重新输入密钥: ").strip()
            verify_result = ai.verify_key(answer)
            print(verify_result["message"])
            
            if not verify_result["passed"]:
                print("验证失败，程序退出")
                return
    
    # 初始化AI
    if ai.initialize():
        print("Cooker AI 初始化成功!")
        print("输入 'exit' 退出程序")
        print("输入 'status' 查看状态")
        print("输入 'web' 启动Web界面")
        print("-" * 30)
        
        # 交互循环
        while True:
            try:
                user_input = input(f"{ai.creator_code} >> ").strip()
                
                if user_input.lower() in ['exit', 'quit', '退出']:
                    print("Cooker AI 关闭中...")
                    break
                elif user_input.lower() == 'status':
                    status = ai.get_status()
                    print(f"状态: {status}")
                    continue
                elif user_input.lower() == 'web':
                    web_info = start_web_interface()
                    print(f"Web界面: {web_info}")
                    continue
                
                # 处理消息
                response = ai.process_message(
                    user_input, 
                    user=ai.creator_code,
                    exposure_level="Lv.0"  # 默认暴露等级
                )
                
                print(f"Cooker >> {response}")
                
            except KeyboardInterrupt:
                print("\n程序被中断")
                break
            except Exception as e:
                print(f"错误: {e}")
                continue

if __name__ == "__main__":
    main()
