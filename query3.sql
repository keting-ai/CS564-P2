select count(*)
    from(
        select count(*) as cat_num
            from Categories
            group by Categories.ItemID)
    where cat_num = 4;