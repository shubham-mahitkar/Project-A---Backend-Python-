# Sql Query

# SQL_QUERY = '''
# CREATE TABLE `tbl_user` (
#   `user_id` bigint COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
#   `user_name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `user_email` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   `user_password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
#   PRIMARY KEY (`user_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'''

from ariadne import QueryType

query = QueryType()