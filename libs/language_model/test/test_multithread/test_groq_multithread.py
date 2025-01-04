import asyncio

from groq import AsyncGroq


async def make_request(client, worker_num):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Writing a 4000 words article about artificial intelligence and its impact on society.",
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    print(f"Worker {worker_num}: {chat_completion.choices[0].message.content}")


async def main():
    client = AsyncGroq()
    tasks = []
    
    # Create 20 concurrent requests
    for i in range(20):
        task = asyncio.create_task(make_request(client, i+1))
        tasks.append(task)
    
    # Wait for all requests to complete
    await asyncio.gather(*tasks)

asyncio.run(main())