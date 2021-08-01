CREATE TABLE IF NOT EXISTS role_lock (
    gid BIGINT,
    command VARCHAR,
    roles BIGINT[]
)

|