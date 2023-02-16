import asyncio

from asyncua import Client




url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"



async def main(tQueue):

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:MyVariable"]
        )
        value = await var.read_value()
        print(f"Value of MyVariable ({var}): {value}")

        new_value = value - 50
        print(f"Setting value of MyVariable to {new_value} ...")
        await var.write_value(new_value)

        task = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:MyObject", f"{nsidx}:TaskArray"]
        )
        task_Str = await task.read_value()

        new_tStr = tQueue
        await task.write_value(new_tStr)
        print(task_Str)

        # Calling a method
        res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
        print(f"Calling ServerMethod returned {res}")


if __name__ == "__main__":
    asyncio.run(main())