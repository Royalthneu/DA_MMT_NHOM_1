#!/bin/bash

# Chạy tất cả các file Python trong thư mục /app
for file in /app/*.py; do
    python "$file" &
done

# Chờ các tiến trình hoàn thành (để giữ container hoạt động)
wait
