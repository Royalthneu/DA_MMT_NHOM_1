# Sử dụng hình ảnh Windows Server Core
FROM mcr.microsoft.com/windows/servercore:ltsc2022

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Thiết lập biến môi trường
ENV PYTHON_VERSION 3.13.0

# Tải Python 3.13 và cài đặt
RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}-amd64.exe' -f ($env:PYTHON_VERSION -replace '[a-z]+[0-9]*$', ''), $env:PYTHON_VERSION); \
    Write-Host ('Downloading {0} ...' -f $url); \
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -Uri $url -OutFile 'python.exe'; \
    Write-Host 'Installing ...'; \
    $exitCode = (Start-Process python.exe -Wait -NoNewWindow -PassThru \
        -ArgumentList @( \
            '/quiet', \
            'InstallAllUsers=1', \
            'TargetDir=C:\Python', \
            'PrependPath=1', \
            'Shortcuts=0', \
            'Include_doc=0', \
            'Include_pip=1', \
            'Include_test=0' \
        ) \
    ).ExitCode; \
    if ($exitCode -ne 0) { \
        Write-Host ('Running python installer failed with exit code: {0}' -f $exitCode); \
        exit $exitCode; \
    } \
    $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); \
    Write-Host 'Verifying install ...'; \
    Write-Host '  python --version'; python --version; \
    Write-Host 'Removing ...'; \
    Remove-Item python.exe -Force; \
    Write-Host 'Complete.'

# Sao chép toàn bộ thư mục server vào container
COPY server /app

# Chuyển đến thư mục /app
WORKDIR /app

# Cài đặt các gói yêu cầu từ requirements.txt, nếu có
# RUN if (Test-Path requirements.txt) { pip install -r requirements.txt }
RUN pip install pyautogui
RUN pip install pillow

# Mở cổng 8080 để server có thể nghe
EXPOSE 8080

# Chạy file server.py
CMD ["python", "server.py"]
