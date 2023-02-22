drop table if exists Items;
drop table if exists Users;
drop table if exists Bids;
drop table if exists Categories;
create table Items(
    ItemID INTEGER PRIMARY KEY,
    SellerID CHAR(128),
    Name CHAR(128),
    Currently DECIMAL,
    First_Bid DECIMAL,
    Number_of_Bids INTEGER,
    Started TIMESTAMP,
    Ends TIMESTAMP,
    Buy_Price DECIMAL,
    Description TEXT,
    FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);
create table Bids(
    ItemID INTEGER,
    UserID CHAR(128),
    Time TIMESTAMP,
    Amount DECIMAL,
    PRIMARY KEY(ItemID, UserID, Time, Amount),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
create table Users(
    UserID CHAR(128) PRIMARY KEY,
    Location CHAR(128),
    Country CHAR(128),
    Rating INTEGER
);
create table Categories(
    ItemID INTEGER,
    Category_Name CHAR(128),
    PRIMARY KEY(ItemID, Category_Name),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);
