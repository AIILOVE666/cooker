from modelscope.hub.snapshot_download import snapshot_download

# 下载ChatGLM3-6B 4bit量化版（适配1650 Ti）
model_dir = snapshot_download(
    "ZhipuAI/chatglm3-6b-4bit",  # 量化版模型名称
    cache_dir="./chatglm3_model"  # 下载到当前目录的chatglm3_model文件夹
)
print(f"模型下载完成，路径：{model_dir}")