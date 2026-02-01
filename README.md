# 简易版 PostgreSQL MCP Server

这是一个精简的 PostgreSQL Model Context Protocol (MCP) 服务器，旨在提供基础的数据库交互和查询分析功能。

## 工具说明

-   **query_sql**
    -   **功能**: 执行通用的 SQL 查询。
    -   **参数**: `sql` (string) - 要执行的 SQL 语句。
    -   **返回**: JSON 格式的查询结果或执行状态消息。

-   **list_tables**
    -   **功能**: 列出数据库中的表。
    -   **参数**: `schema` (string, 默认 "public") - 要查询的模式名称。
    -   **返回**: 包含表名和表类型的 JSON 列表。

-   **describe_table**
    -   **功能**: 获取表的详细结构信息。
    -   **参数**: 
        -   `table_name` (string) - 表名。
        -   `schema` (string, 默认 "public") - 模式名称。
    -   **返回**: 包含列名、数据类型、可空性、默认值等信息的 JSON 列表。

-   **explain_query**
    -   **功能**: 分析 SQL 查询计划，支持虚拟索引。
    -   **参数**:
        -   `sql` (string) - 要分析的 SQL 语句。
        -   `analyze` (boolean, 默认 false) - 是否实际执行查询 (EXPLAIN ANALYZE)。
        -   `hypothetical_indexes` (list[string], 可选) - 虚拟索引定义列表 (需要 hypopg 扩展)。
    -   **返回**: JSON 格式的查询计划。


## 快速开始 (使用 uv)

本项目支持通过 `uv` 直接运行，无需手动安装依赖（依赖已声明在脚本头部）。

```bash
# 进入目录
cd postgresql-mcp

# 直接运行（uv 会自动安装 mcp 和 psycopg 依赖）
# 确保设置了环境变量
set DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb
uv run server.py
```

## 配置

### 环境变量

您可以使用以下任意一种方式配置数据库连接：

1.  **方式 A (推荐): 使用 `DATABASE_URL`**
    ```bash
    set DATABASE_URL=postgresql://user:password@localhost:5432/dbname
    ```

2.  **方式 B: 使用标准 PG 环境变量**
    如果未设置 `DATABASE_URL`，服务器将自动读取以下变量：
    - `PGUSER`: 用户名
    - `PGPASSWORD`: 密码
    - `PGHOST`: 主机地址 (默认 localhost)
    - `PGPORT`: 端口 (默认 5432)
    - `PGDATABASE`: 数据库名

### MCP 客户端配置示例

#### Claude Desktop / Trae 配置

请将以下配置添加到您的 MCP 配置文件中 (如 `claude_desktop_config.json` 或 Trae 的配置)：

```json
{
  "mcpServers": {
    "postgresql": {
      "command": "uv",
      "args": [
        "run",
        "E:\\OpenProjectCode\\testPython\\postgresql-mcp\\server.py"
      ],
      "env": {
        "PGUSER": "your_username",
        "PGPASSWORD": "your_password",
        "PGHOST": "localhost",
        "PGPORT": "5432",
        "PGDATABASE": "your_dbname"
      }
    }
  }
}
```

> **注意**: 
> 1. 请确保 `uv` 命令在您的系统 PATH 中。
> 2. 将 `args` 中的路径修改为您实际的 `server.py` 绝对路径。
> 3. 您也可以在 `env` 中直接使用 `"DATABASE_URL": "postgresql://..."` 替代 PG* 变量。

## 虚拟索引分析示例

要使用虚拟索引分析，您的 PostgreSQL 数据库必须安装 `hypopg` 扩展：

```sql
-- 在数据库中执行
CREATE EXTENSION hypopg;
```

然后在 MCP 客户端中调用 `explain_query` 工具：

- **sql**: `SELECT * FROM my_table WHERE col_a = 123`
- **hypothetical_indexes**: `["CREATE INDEX ON my_table (col_a)"]`
- **analyze**: `false` (虚拟索引不支持 analyze)

服务器将模拟创建索引并返回查询计划，您可以对比 Cost 值来评估索引效果。
