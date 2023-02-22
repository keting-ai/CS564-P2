select count (distinct SellerID)
    from Items, Users
    where Rating > 1000 and UserID = SellerID;