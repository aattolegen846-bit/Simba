from concurrent.futures import ThreadPoolExecutor
import os


# Reduce thread pool size to prevent CPU overload
_max_workers = int(os.getenv("ASYNC_MAX_WORKERS", "2"))
_executor = ThreadPoolExecutor(max_workers=_max_workers, thread_name_prefix="simpai-bg")


def dispatch_background_task(fn, *args, **kwargs) -> None:
    _executor.submit(fn, *args, **kwargs)
