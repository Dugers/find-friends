from .conn import get_conn


async def delete_like(id=False):
    conn = await get_conn()
    if id:
        res = await conn.execute('DELETE FROM likes WHERE id = $1', id)
    await conn.close()
    return res