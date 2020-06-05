create table if not exists "user" (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
create table if not exists house (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL
);
create table if not exists task (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    house_id INTEGER NOT NULL REFERENCES house (id),
    "description" TEXT NOT NULL,
    frequency INTEGER NOT NULL
);
create table if not exists user_task (
    id SERIAL PRIMARY KEY,
    user_id integer not null references "user" (id),
    task_id integer not null references task (id),
    deadline integer not null,
    done boolean not null
);
create table if not exists user_houses (
    user_id integer not null references "user" (id) on delete cascade,
    house_id integer not null references house (id) on delete cascade,
    primary key (user_id, house_id)
);
CREATE TABLE IF NOT EXISTS worker_task (
    id SERIAL PRIMARY KEY,
    complete_at TIMESTAMP NOT NULL,
    task_type INTEGER NOT NULL,
    context TEXT NOT NULL
);