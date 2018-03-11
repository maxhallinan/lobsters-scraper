# delete lobsters database
psql -a -f queries/drop_db_lobsters.sql
# create lobsters database
psql -a -f queries/create_db_lobsters.sql
# create stories table
psql -d lobsters -a -f queries/create_table_stories.sql
# create stories_tags table
psql -d lobsters -a -f queries/create_table_stories_tags.sql
# create stories_users table
psql -d lobsters -a -f queries/create_table_stories_users.sql
# create tags table
psql -d lobsters -a -f queries/create_table_tags.sql
# create users table
psql -d lobsters -a -f queries/create_table_users.sql
# put data into database
python scripts/insert_rows.py ./data/csv
