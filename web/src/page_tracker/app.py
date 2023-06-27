# src/page_tracker/app.py

import os
import time
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    try:
        start = time.time()
        page_views = redis().incr("page_views")
        end = time.time()
        app.logger.info("Redis operation took %s seconds.", end - start)
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{thinking face}", 500
    else:
        return f"This page has been seen {page_views} times."


@cache
def redis():
    # return Redis()
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
