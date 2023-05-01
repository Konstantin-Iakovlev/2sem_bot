create table words(
    id integer primary key,
    src varchar(255),
    trg varchar(255),
    created datetime
);

insert into words (src, trg, created)
values
    ("alignment", "выравнивание", "2023-01-01 10:00:00"),
    ("chance", "шанс", "2023-01-01 10:00:01"),
    ("wait", "ждать", "2023-01-01 10:00:02"),
    ("think", "думать", "2023-01-01 10:00:03"),
    ("integrity", "честность", "2023-01-01 10:00:04"),
    ("follow", "следовать", "2023-01-01 10:00:05");
