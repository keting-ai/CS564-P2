select count (distinct Category_Name)
from Categories, Bids
where Bids.ItemID = Categories.ItemID and Bids.Amount > 100;