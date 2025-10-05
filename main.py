from flask import Flask, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from services import pyocr_service

app = Flask(__name__)

# 配置上传文件夹和允许的扩展名
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否合法"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    # 获取查询参数
    ocr_type = request.args.get('type', default='default', type=str)

    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # 检查是否选择了文件
    if file.filename == '' or file.filename is None:
        return jsonify({"error": "No selected file"}), 400
    
    # 检查文件类型
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存临时文件
        file.save(temp_path)
        
        try:
            if ocr_type == 'default':
                # 使用 pyocr 处理
                result = pyocr_service.readimg(temp_path)
            else:
                return jsonify({"error": "Unknown ocr type."}), 400
            
            # 返回处理结果
            return jsonify({"result": result}), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)