from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    raise Exception('My life is meaningless')
    return f"Hello, {name}!"
    
