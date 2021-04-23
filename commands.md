# Connect to local food_delivery db
psql food_delivery malik

# Create Postgres backup of local database
PGPASSWORD='<password>' pg_dump -Fc --no-acl --no-owner -h localhost -U '<user_name>' food_delivery > food_delivery.dump

# Get heroku app credentials
heroku pg:credentials:url -a infinite-beach-27814

# Import local postgres backup to heroku 
pg_restore --verbose --clean --no-acl --no-owner -h ec2-3-234-85-177.compute-1.amazonaws.com -U cumvkrupswcgdd -d d493rlg8h9i5p9 -p 5432 food_delivery.dump


