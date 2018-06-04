select date, callsign, count(Date) as 'Times Heard' from staging
group by callsign, date
order by date desc, callsign asc
