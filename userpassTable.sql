use c9;

drop table if exists userpass;

create table userpass(
       username varchar(50) not null primary key,
       hashed char(60)
);