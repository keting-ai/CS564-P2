create view both as 
    select ItemID, max(Currently)
    from Items;
select ItemID from both;