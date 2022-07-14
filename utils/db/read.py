from .conn import get_conn

async def get_users(one=False, telegram_id=None, city_id=None, checked=None, find_sex=None):
    conn = await get_conn()
    if one:
        res = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
    elif city_id:
        checked = tuple(checked)
        find_sex = tuple(find_sex)
        if len(checked) == 1:
            checked = f"({checked[0]})"
        if len(find_sex) == 1:
            find_sex = f"({find_sex[0]})"
        res = await conn.fetchrow(f"SELECT * FROM users WHERE (city_id = $1) AND (telegram_id NOT IN {checked}) AND (sex IN {find_sex})", city_id)
    await conn.close()
    return res

async def get_city(id=False, name=False, all=False):
    conn = await get_conn()
    if name:
        res = await conn.fetchrow('SELECT * FROM cities WHERE name = $1', name)
    elif id:
        res = await conn.fetchrow('SELECT * FROM cities WHERE id = $1', id)
    elif all:
        res = await conn.fetch('SELECT * FROM cities')
    await conn.close()
    return res


async def get_like(recipient_id=False):
    conn = await get_conn()
    if recipient_id:
        res = await conn.fetchrow('SELECT * FROM likes WHERE recipient = $1', recipient_id)
    await conn.close()
    return res