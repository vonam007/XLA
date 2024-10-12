# Image Processing Web App

Một ứng dụng web cho phép người dùng tải lên hình ảnh và thực hiện các xử lý ảnh cơ bản như chuyển đổi màu sắc, làm mịn, làm sắc nét và phát hiện cạnh.

## Mục tiêu

- Tải lên hình ảnh.
- Áp dụng các phương pháp xử lý ảnh.
- Hiển thị ảnh gốc và các ảnh đã xử lý.

## Công nghệ sử dụng

- Flask: Framework web cho Python.
- OpenCV: Thư viện xử lý ảnh.
- NumPy: Thư viện hỗ trợ tính toán số.

## Cài đặt

1. **Create VENV:**

    ```bash
    python -m venv venv
    venv\Scripts\activate 
    ```

2. **Install requirements:**

    ```bash
    pip install -r requirements.txt
    ```

## Chạy ứng dụng:
1. **Chạy FLASK_APP:**

    ```bash
    python app.py
    ```

2. **Mở browser:**

    ```bash
    http://127.0.0.1:5000
    ```


## Cách sử dụng
1. Tải lên một hình ảnh từ máy tính của bạn.
2. Chọn phương pháp xử lý ảnh từ danh sách.
3. Nhấn nút "Upload and Process" để xem kết quả.

## Thư mục dự án
- uploads/: Thư mục chứa ảnh đã tải lên.
- static/: Thư mục chứa ảnh đã xử lý và các tệp tĩnh khác (CSS, JS).
- app.py: Tệp chính của ứng dụng Flask.
- requirements.txt: Danh sách các thư viện cần thiết.