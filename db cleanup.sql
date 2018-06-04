select * from staging
where
callsign like 'DAL%' or callsign like 'UAL%'


delete from staging
where
callsign like 'DAL%' or callsign like 'UAL%'

select distinct callsign from staging
order by callsign


