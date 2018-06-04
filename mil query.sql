select distinct callsign from staging
where callsign like '[A-Z][A-Z][A-Z][A-Z]%' or
callsign like 'RCH%'
order by Callsign



