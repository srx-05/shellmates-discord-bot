# main.py
from  database.connection  import Database  # الكلاس اللي عملتيه
from  database.repositories.usersrepo import UserRepository  # مسار الملف حسب مشروعك

# إنشاء Pool للاتصالات
db = Database()

# إنشاء المستودع
user_repo = UserRepository(db)

# ====== إضافة مستخدم ======
user_id = user_repo.add_user("123456789", "Alice")
print(f"✅ Added user with ID: {user_id}")

# ====== جلب مستخدم بواسطة Discord ID ======
user = user_repo.get_user_by_discord_id("123456789")
print("User info:", user)

# ====== تحديث اسم المستخدم ======
success = user_repo.update_username(user_id, "AliceUpdated")
if success:
    print("✅ Username updated successfully")

# ====== جلب كل المستخدمين (مع Pagination) ======
all_users = user_repo.get_all_users(limit=10, offset=0)
print("All users:", all_users)

# ====== حذف المستخدم ======
#deleted = user_repo.delete_user(user_id)
#if deleted:
 #   print("✅ User deleted successfully")

# غلق كل الاتصالات عند الانتهاء
db.close_all_connections()