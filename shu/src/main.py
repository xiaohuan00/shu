import os
import zhipuai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# 加载环境变量（支持本地开发和 Replit）
if os.path.exists('.env'):
    load_dotenv()
api_key = os.getenv('ZHIPUAI_API_KEY')

app = Flask(__name__, 
    static_url_path='/static',
    static_folder='static'  # Replit 中不需要 ../src 前缀
)

class XiaohongshuTitleGenerator:
    def __init__(self):
        api_key = os.getenv('ZHIPUAI_API_KEY')
        if not api_key:
            raise ValueError("未找到 ZHIPUAI_API_KEY 环境变量")
        self.client = zhipuai.ZhipuAI(api_key=api_key)
    
    def chat(self, message):
        try:
            response = self.client.chat.completions.create(
                model="glm-4",
                messages=[
                    {"role": "system", "content": """你是小红书标题创作专家。请遵循以下规则：
                    1. 目标受众：年轻群体（18-35岁，主要是女性）
                    2. 标题要求：
                       - 字数限制：20字以内
                       - 数量：3-5个备选
                       - 必须包含实质内容，避免'来看看吧'等空泛表达
                       - 每个标题都要带上合适的emoji
                    3. 创作指南：
                       - 优先输出与关键词高度相关的内容
                       - 鼓励尝试不同风格（如幽默、悬念、干货、种草等）
                       - 可以适当加入创意表达，但不偏离主题
                    如果用户有特殊要求（如具体数量、风格），优先满足用户需求。"""},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"错误：{str(e)}"

generator = XiaohongshuTitleGenerator()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "缺少prompt参数"}), 400
        
        response = generator.chat(data['prompt'])
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Replit 使用 3000 端口
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)