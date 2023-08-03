import db_fns
b2_db_cursor = db_fns.b2_db_cursor
res = b2_db_cursor.execute("SELECT UserId FROM Matches")
print(len(res.fetchall()))