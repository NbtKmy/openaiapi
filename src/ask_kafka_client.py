import asyncio
import dotenv
import os
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

dotenv.load_dotenv()

async def main():

    dir_path = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(dir_path, "kafka_brief_an_den_vater.py")
    transport = PythonStdioTransport(script_path=server_script)

    async with Client(transport) as client:
        # 利用可能なツールを取得
        tools = await client.list_tools()
        print("ツール:" ,tools)

        # ツールの呼び出し
        result = await client.call_tool("search", {"query": "Wie ist die Beziehung zwischen Kafka und seinem Vater?", "k": 3})
        print("ツール呼び出し結果:", result)

if __name__ == "__main__":
    asyncio.run(main())