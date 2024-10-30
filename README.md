**Cài đặt dockerfile cho server ảo**

docker build -t python-server .

**Khởi động server docker và mở port 8080**

docker run -p 8080:8080 python-server

