from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, flash
import cv2
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thêm secret key cho flash messages

# Thư mục để lưu file upload và file xử lý
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    original_image = 'uploaded_image.jpg' if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')) else None
    # Lấy danh sách phương pháp đã xử lý từ query string
    processed_methods = request.args.getlist('processed_images')  # Dùng getlist để lấy tất cả phương pháp đã xử lý

    # Khởi tạo từ điển cho ảnh đã xử lý
    processed_images = {}
    
    # Kiểm tra từng phương pháp và thêm vào từ điển nếu tồn tại ảnh
    for method in processed_methods:
        if method in ['sobel', 'prewitt', 'canny', 'smoothing', 'sharpening']:
            image_filename = f'output_{method}.jpg'  # Tạo tên file tương ứng
            if os.path.exists(os.path.join(app.config['OUTPUT_FOLDER'], image_filename)):
                processed_images[method] = image_filename  # Thêm vào từ điển nếu tồn tại

    return render_template('index.html', original_image=original_image, processed_images=processed_images)


# Route để lấy ảnh gốc từ thư mục uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_image():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')

    # Kiểm tra nếu không có file mới được chọn, sẽ sử dụng ảnh cũ
    if 'file' not in request.files or request.files['file'].filename == '':
        if not os.path.exists(original_image_path):
            return render_template('index.html', error="Please upload an image file.", original_image=None, processed_images=None)
        else:
            # Nếu có ảnh cũ, không cần lưu ảnh mới
            img = cv2.imread(original_image_path)
    else:
        file = request.files['file']
        file.save(original_image_path)  # Lưu ảnh mới
        img = cv2.imread(original_image_path)

    method = request.form['method']
    processed_images = []

    if method == 'smoothing':
        # Xử lý ảnh: smoothing
        smooth_img = cv2.GaussianBlur(img, (5, 5), 0)
        output_smooth_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_smoothing.jpg')
        cv2.imwrite(output_smooth_path, smooth_img)
        processed_images.append('smoothing')

    elif method == 'sharpening':
        # Xử lý ảnh: sharpening
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharpened_img = cv2.filter2D(img, -1, kernel)
        output_sharpen_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_sharpening.jpg')
        cv2.imwrite(output_sharpen_path, sharpened_img)
        processed_images.append('sharpening')

    elif method == 'edge_detection':
        # Xử lý ảnh: edge detection (Sobel, Prewitt, Canny)
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
        output_sobel_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_sobel.jpg')
        cv2.imwrite(output_sobel_path, cv2.magnitude(sobelx, sobely))

        # Prewitt filter
        prewitt_kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        prewitt_kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        img_prewittx = cv2.filter2D(img, -1, prewitt_kernel_x).astype(np.float32)
        img_prewitty = cv2.filter2D(img, -1, prewitt_kernel_y).astype(np.float32)
        output_prewitt_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_prewitt.jpg')
        prewitt_magnitude = np.sqrt(np.power(img_prewittx, 2) + np.power(img_prewitty, 2)).astype(np.uint8)
        cv2.imwrite(output_prewitt_path, prewitt_magnitude)

        # Canny edge detection
        output_canny_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_canny.jpg')
        img_canny = cv2.Canny(img, 100, 200)
        cv2.imwrite(output_canny_path, img_canny)

        processed_images.extend(['sobel', 'prewitt', 'canny'])

    return redirect(url_for('index', processed_images=processed_images))

if __name__ == '__main__':
    app.run(debug=True)
