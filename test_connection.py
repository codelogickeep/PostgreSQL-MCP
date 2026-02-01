# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]",
#     "psycopg[binary]>=3.2.0",
# ]
# ///

import os
import asyncio
import sys

# 将当前目录添加到 sys.path 以便导入 server.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 在导入 server 之前设置环境变量，模拟用户场景
# 注意：PGUSER 和 PGPASSWORD 将从系统环境变量中继承（如果已设置）
os.environ["PGHOST"] = "localhost"
os.environ["PGPORT"] = "5432"
os.environ["PGDATABASE"] = "zhigu_db"
os.environ["PGCONNECT_TIMEOUT"] = "5" # 设置 5 秒超时，避免一直等待

# 确保 DATABASE_URL 不存在，强制 server.py 使用 PG* 环境变量
if "DATABASE_URL" in os.environ:
    del os.environ["DATABASE_URL"]

from server import get_connection

async def test():
    print("=== PostgreSQL 连接测试 ===")
    print("正在尝试连接数据库，使用以下配置：")
    print(f"  PGHOST:     {os.environ.get('PGHOST')}")
    print(f"  PGPORT:     {os.environ.get('PGPORT')}")
    print(f"  PGDATABASE: {os.environ.get('PGDATABASE')}")
    print(f"  PGUSER:     {os.environ.get('PGUSER', '<未设置，将使用系统默认>')}")
    print(f"  PGPASSWORD: {'******' if os.environ.get('PGPASSWORD') else '<未设置>'}")
    print("-" * 30)

    try:
        conn = await get_connection()
        print("\n✅ 连接成功！")
        print(f"  当前数据库: {conn.info.dbname}")
        print(f"  当前用户:   {conn.info.user}")
        print(f"  服务器版本: {conn.info.server_version}")
        
        await conn.close()
        print("\n连接已关闭。")
    except Exception as e:
        print("\n❌ 连接失败！")
        print(f"错误信息: {e}")
        print("\n提示: 请检查您的系统环境变量中是否已正确设置 PGUSER 和 PGPASSWORD，以及数据库是否正在运行。")

if __name__ == "__main__":
    # Windows 下 psycopg 需要使用 SelectorEventLoop
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test())
