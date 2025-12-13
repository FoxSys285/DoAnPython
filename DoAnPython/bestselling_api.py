from flask import Flask, jsonify
from collections import defaultdict
import json
import os

# 1. Khởi tạo ứng dụng Flask
app = Flask(__name__)
# Đặt cấu hình Pretty Print ngay sau khi khởi tạo app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Tên file dữ liệu của bạn
DATA_FILE = 'data/du_lieu_hoa_don.json'

def calculate_best_selling_items(data):
    """
    Tính toán và trả về danh sách 5 món bán chạy nhất.
    """
    # Sử dụng defaultdict để lưu trữ tổng số lượng bán của từng món
    item_sales = defaultdict(int)
    item_details = {}  # Lưu trữ chi tiết món (tên, đơn giá, loại)

    for hoa_don in data:
        for mon in hoa_don.get('dsMon', []):
            ma_mon = mon['ma_mon']
            so_luong = mon['so_luong']

            # Tăng tổng số lượng bán
            item_sales[ma_mon] += so_luong
            
            # Lưu chi tiết món lần đầu tiên gặp (hoặc cập nhật nếu cần)
            if ma_mon not in item_details:
                item_details[ma_mon] = {
                    'ma_mon': mon['ma_mon'],
                    'ten_mon': mon['ten_mon'],
                    'loai': mon['loai'],
                    # Có thể thêm các trường khác nếu muốn
                }

    # Chuyển đổi từ dictionary sang list để dễ dàng sắp xếp
    sales_list = []
    for ma_mon, total_sold in item_sales.items():
        details = item_details[ma_mon]
        sales_list.append({
            'ma_mon': ma_mon,
            'ten_mon': details['ten_mon'],
            'loai': details['loai'],
            'tong_so_luong_ban': total_sold
        })

    # 2. Sắp xếp danh sách theo 'tong_so_luong_ban' giảm dần
    sorted_sales = sorted(sales_list, key=lambda x: x['tong_so_luong_ban'], reverse=True)

    # 3. Trả về 5 món bán chạy nhất
    return sorted_sales[:5]

@app.route('/api/v1/best-selling/top5', methods=['GET'])
def get_top_5_best_selling():
    """
    Endpoint để trả về 5 món bán chạy nhất.
    """
    
    try:
        # Kiểm tra xem file dữ liệu có tồn tại không
        if not os.path.exists(DATA_FILE):
            return jsonify({'error': 'Không tìm thấy file dữ liệu: ' + DATA_FILE}), 500

        # Đọc dữ liệu từ file JSON
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            hoa_don_data = json.load(f)

        # Tính toán kết quả
        top_5_items = calculate_best_selling_items(hoa_don_data)

        # Trả về kết quả dưới dạng JSON
        return jsonify({
            'success': True,
            'description': 'Danh sách 5 món bán chạy nhất dựa trên tổng số lượng.',
            'top_items': top_5_items
        }), 200

    except Exception as e:
        # Xử lý các lỗi khác (ví dụ: lỗi parsing JSON)
        print(f"Lỗi khi xử lý dữ liệu: {e}")
        return jsonify({'error': 'Lỗi nội bộ khi xử lý dữ liệu.'}), 500
        
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


#http://127.0.0.1:5000/api/v1/best-selling/top5