select * from rider_rider 
where concat(upper(last_name), ',', upper(first_name)) like 'A%'
