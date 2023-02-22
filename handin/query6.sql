select count (distinct UserID)
    from Items, Bids
    where SellerID = UserID;