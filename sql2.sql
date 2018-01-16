create table Users(
	uid int AUTO_INCREMENT,
    username varchar(25),
    password nvarchar(25),
    email nvarchar(25),
    address nvarchar(50),
    mobile nvarchar(20),
    deposit int,
    PRIMARY KEY (uid)
);

create table bitcoinvalues (
	bvid int auto_increment,
    buying_price decimal,
    selling_price decimal,
    primary key (bvid)
);

create table trades (
	tid int auto_increment,
    trade_date date,
    userid int,
    bitcoinid int,
    primary key (tid),
    foreign key (userid) references Users(uid),
    foreign key (bitcoinid) references bitcoinvalues(bvid)
);


create table messages (
	mid int auto_increment,
    message nvarchar(150),
    userid int,
    primary key (mid),
    foreign key (userid) references Users(uid)
    )
    
select Users.uid, Users.username from Users inner join trades on Users.uid = trades.userid;
