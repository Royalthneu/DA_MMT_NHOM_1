# Sử dụng image Python 3.13 chính thức
FROM python:3.13-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả file từ thư mục `server` vào container
COPY . /app

# Cài đặt các gói yêu cầu từ `requirements.txt`, nếu có
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Sao chép và thiết lập quyền thực thi cho entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Mở cổng 8080 để server có thể nghe
EXPOSE 8080

# Sử dụng entrypoint.sh để chạy tất cả file Python
CMD ["/app/entrypoint.sh"]
