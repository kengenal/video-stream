def send_bytes_range(path: str, start: int, end: int, chunk_size: int = 10_000):
    with open(path, mode="rb") as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def send_bytes_file(path: str):
    with open(path, mode="rb") as f:
        yield from f
