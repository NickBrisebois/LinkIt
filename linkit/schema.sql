drop table if exists posts;
create table posts (
	id integer primary key autoincrement,
	title text not null,
	postDate text not null,
	postContents text not null,
	postLink text
);
