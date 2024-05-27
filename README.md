# Rides API (Wingz Developer Test)

This project implements a RESTful API for managing ride information using Django.

## Setup
```bash
docker-compose up --build
```
This will install all packages in `requirements.txt`, run migrations, and bring up the web server at http://localhost:8000.

## Running Tests
```bash
docker-compose run web python manage.py test rides.tests
```

## Performance Notes
### Ensuring Efficient Database Queries
In views/ride_views.py, the database queries will be optimized as follows:
1. First SQL Query: Retrieves the rides along with related rider and driver using `select_related`.
2. Second SQL Query: Uses `prefetch_related` to retrieve `RideEvent` objects filtered to the last 24 hours.

## BONUS: SQL Query
The thought-process is:
1. Join the `rides_ride` table with the `rides_rideevent` table twice to get the pickup and dropoff events.
2. Then, filter the trips where the difference between the dropoff and pickup time is strictly greater than 1 hour.
3. Next, group the results by month and driver.
4. Finally, count the number of trips for each month and driver.

```sql
SELECT 
    DATE_TRUNC('month', r.pickup_time) AS month,
    r.driver_id AS driver_id,
    COUNT(*) AS trip_count
FROM 
    rides_ride r
JOIN 
    rides_rideevent pe ON r.id = pe.ride_id AND pe.description = 'Status changed to pickup'
JOIN 
    rides_rideevent de ON r.id = de.ride_id AND de.description = 'Status changed to dropoff'
WHERE 
    de.created_at - pe.created_at > INTERVAL '1 hour'
GROUP BY 
    month, driver_id
ORDER BY 
    month, driver_id;
```
