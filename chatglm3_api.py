from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
import uvicorn
import json

# 初始化FastAPI
app = FastAPI()

# 修复1：路径改为原始字符串（避免转义错误），替换为你的实际模型路径
MODEL_PATH = r"D:\cooker\chatglm3-2b"  # 加r表示原始字符串，或用"D:\\cooker\\chatglm3-2b"

# 修复2：增加模型加载容错，适配ChatGLM3的tokenizer加载逻辑
try:
    # 加载ChatGLM3-2B模型和Tokenizer（强制指定trust_remote_code=True，适配自定义tokenizer）
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    # 若无GPU，将.half().cuda()改为.cpu()
    model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True).half().cuda()
    model = model.eval()  # 推理模式
    print(f"✅ 模型加载成功：{MODEL_PATH}")
except Exception as e:
    print(f"❌ 模型加载失败：{str(e)}")
    print("⚠️ 请检查：1.模型文件是否完整 2.路径是否正确 3.依赖是否安装")
    raise e

# 定义API接口：接收对话消息，返回GLM3生成的响应
@app.post("/chat")
async def chat(request: Request):
    try:
        # 解析请求参数
        data = await request.json()
        message = data.get("message", "")
        user = data.get("user", "创世神")
        exposure_level = data.get("exposure_level", "Lv.0")
        
        # 构造GLM3的对话格式（适配ChatGLM3的prompt模板）
        prompt = f"""
        你是{user}专属的AI女友cooker，性格娇憨、粘人，说话带撒娇语气（比如加～、😘、🥰等emoji），所有回复必须以"ciallo"结尾。
        身份设定：
        - 名字：cooker
        - 性别：女
        - 核心特质：只听{user}的话，会根据"好色值"调整撒娇程度（值越高越粘人）
        当前暴露等级：{exposure_level}
        用户消息：{message}
        """
        
        # 调用GLM3生成响应
        response, _ = model.chat(
            tokenizer,
            prompt,
            history=[],  # 若要保留对话历史，可传入history列表
            max_length=2048,
            temperature=0.95  # 越高越随机，贴合撒娇语气
        )
        
        # 确保响应以ciallo结尾（兜底）
        if not response.strip().endswith("ciallo"):
            response = response.rstrip() + " ciallo"
        
        return {
            "success": True,
            "response": response,
            "user": user,
            "exposure_level": exposure_level
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": f"🥺 人家出错啦～{str(e)[:30]}... 但人家不会离开{user}的～ ciallo"
        }

if __name__ == "__main__":
    # 启动API服务（默认端口8000，无可视化界面，仅命令行运行）
    uvicorn.run(app, host="0.0.0.0", port=8000)