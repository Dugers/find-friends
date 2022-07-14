from .conn import get_conn

async def update_user(telegram_id, name=False, age=False, username=False, sex=False, find_sex=False, photo_id=False, video_id=False, description=False, city_id=False, checked=False, check_time=False):
    conn = await get_conn()
    if name:
        await conn.execute('UPDATE users SET name = $1 WHERE telegram_id = $2', name, telegram_id)
    if age:
        await conn.execute('UPDATE users SET age = $1 WHERE telegram_id = $2', age, telegram_id)
    if username:
        await conn.execute('UPDATE users SET username = $1 WHERE telegram_id = $2', username, telegram_id)
    if sex:
        await conn.execute('UPDATE users SET sex = $1 WHERE telegram_id = $2', sex, telegram_id)
    if find_sex:
        await conn.execute('UPDATE users SET find_sex = $1 WHERE telegram_id = $2', find_sex, telegram_id)
    if photo_id or photo_id is None:
        await conn.execute('UPDATE users SET photo_id = $1 WHERE telegram_id = $2', photo_id, telegram_id)
    if video_id or video_id is None:
        await conn.execute('UPDATE users SET video_id = $1 WHERE telegram_id = $2', video_id, telegram_id)
    if description or description is None:
        await conn.execute('UPDATE users SET description = $1 WHERE telegram_id = $2', description, telegram_id)
    if city_id:
        await conn.execute('UPDATE users SET city_id = $1 WHERE telegram_id = $2', city_id, telegram_id)
    if checked:
        await conn.execute('UPDATE users SET checked = $1 WHERE telegram_id = $2', checked, telegram_id)
    if check_time:
        await conn.execute('UPDATE users SET check_time = $1 WHERE telegram_id = $2', check_time, telegram_id)
        