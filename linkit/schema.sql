drop table if exists posts;
create table posts (
	id text primary key not null,
	title text not null,
	postDate text not null,
	postContents text not null,
	postLink text
);
