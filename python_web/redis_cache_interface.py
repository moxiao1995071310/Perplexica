# @file    : redis_cache_interface
# @time    : 2025/3/18
# @author  : yongpeng.yao
# @desc    :

import logging
from typing import Optional

import aioredis
from fastapi import FastAPI
from pydantic import BaseModel

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Redis 客户端
redis_client: Optional[aioredis.Redis] = None
# 缓存时间 300秒
CACHE_TTL = 300


class ChatRequest(BaseModel):
    message: str


class SearchRequest(BaseModel):
    query: str


def get_local_chat_response(message: str) -> str:
    # 模拟请求本地链接获取聊天响应
    return f"Local chat response for: {message}"


def get_local_search_response(query: str) -> str:
    # 模拟请求本地链接获取搜索响应
    return f"Local search response for: {query}"


def create_redis_conn_handler():
    async def start_app():
        global redis_client
        redis_client = await aioredis.Redis(
            host="redis",
            db=0,
            encoding="utf-8",
        )

    return start_app


def create_redis_disconnect_handler():
    async def stop_app():
        global redis_client
        await redis_client.close()

    return stop_app


app.add_event_handler("startup", create_redis_conn_handler())
app.add_event_handler("shutdown", create_redis_disconnect_handler())


@app.post("/api/chat")
async def chat(request: ChatRequest):
    cache_key = f"chat:{request.message}"
    cached_response = await redis_client.get(cache_key)

    if cached_response:
        logging.info(f"缓存命中聊天消息: {request.message}")
        return {"message": cached_response}

    logging.info(f"缓存未命中聊天消息: {request.message}")
    local_response = get_local_chat_response(request.message)
    await redis_client.setex(cache_key, CACHE_TTL, local_response)

    return {"message": local_response}


@app.post("/api/search")
async def search(request: SearchRequest):
    cache_key = f"search:{request.query}"
    cached_response = await redis_client.get(cache_key)

    if cached_response:
        logging.info(f"缓存命中搜索查询: {request.query}")
        return {"query": cached_response}

    logging.info(f"缓存未命中搜索查询: {request.query}")
    local_response = get_local_search_response(request.query)
    await redis_client.setex(cache_key, CACHE_TTL, local_response)

    return {"query": local_response}


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
