FROM python:3.9-slim
WORKDIR /home/perplexica

COPY python_web /home/perplexica/python_web

RUN pip3 install -r python_web/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
# 暴露 FastAPI 服务端口
EXPOSE 8000

CMD ["python3", "python_web/redis_cache_interface.py"]
