FROM python:3.9-slim

# 指定 Image 中的工作目錄
WORKDIR /code

# 將 Dockerfile 所在目錄下的所有檔案複製到 Image 的工作目錄 /code 底下
ADD . /code

# 在 Image 中執行的指令：安裝 requirements.txt 中所指定的 dependencies
RUN pip install pymysql==1.0.2
RUN pip install urllib3==1.26.6
RUN pip install selenium==3.141.0
RUN pip install lxml==4.6.3


CMD ["make local-run"]