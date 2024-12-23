import asyncio

from tasks.kafka import consume
from tasks.runner import handle_user_created


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        consume(
            "tasks-service",
            handle_user_created,
            ["users.created"],
        ),
    )
    loop.close()

if __name__ == "__main__":
    main()
