use test;
drop table if exists test.movies ;
create table test.movies
(
	id int auto_increment primary key,
	movie_title varchar(128) null comment 'movie_title',
	movie_type varchar(128) null comment 'movie_type',
	release_date varchar(128) null comment 'release_date'
)
engine=MyISAM charset=utf8;