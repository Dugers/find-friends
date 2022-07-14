from .conn import get_conn

async def create_tables():
    conn = await get_conn()
    await create_table_users(conn)
    await create_table_cities(conn)
    await create_table_likes(conn)
    await conn.close()

async def create_table_users(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            telegram_id bigint,
            username text,
            name text,
            age smallint,
            sex char(1),
            find_sex char(2),
            city_id integer,
            photo_id text,
            video_id text,
            description text,
            checked bigint[],
            check_time bigint
        )
    ''')

async def create_table_cities(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS cities(
            id serial PRIMARY KEY,
            name text,
            coordinates real[]
        )
    ''')

async def create_table_likes(conn):
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS likes(
            id serial PRIMARY KEY,
            sender bigint,
            recipient bigint,
            description text
        )
    ''')

async def create_user(telegram_id, username, name, age, sex, find_sex, city_id, photo_id, video_id, description):
    conn = await get_conn()
    await conn.execute('INSERT INTO users(telegram_id, username, name, age, sex, find_sex, city_id, photo_id, video_id, description) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)', telegram_id, username, name, age, sex, find_sex, city_id, photo_id, video_id, description)
    await conn.close()

async def create_city(name, coordinates):
    conn = await get_conn()
    await conn.execute('INSERT INTO cities(name, coordinates) VALUES($1, $2)', name, coordinates)
    await conn.close()

async def create_like(sender, recipient, description=None):
    conn = await get_conn()
    await conn.execute('INSERT INTO likes(sender, recipient, description) VALUES($1, $2, $3)', sender, recipient, description)
    await conn.close()