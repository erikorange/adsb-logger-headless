select * from staging
where
callsign = 'A24DEF' or
callsign like 'AVLON%' or
callsign like 'BATON%' or
callsign like 'BISON%' or
callsign like 'BOXER%' or
callsign like 'DECOY%' or
callsign like 'EDDIE%' or
callsign like 'GOTO%' or
callsign like 'GOLD%' or
callsign like 'INDY%' or
callsign like 'JENNA%' or
callsign like 'MAGIC%' or
callsign like 'MAINE%' or
callsign like 'MANGO%' or
callsign like 'MFROG%' or
callsign = 'N248CF' or
callsign like 'PACK%' or
callsign like 'PISTOL%' or
callsign like 'POLO%' or
callsign like 'RCH%' or
callsign like 'RESQ%' or
callsign like 'RONPOCH%' or
callsign like 'ROYAL%' or
callsign like 'RUMMY%' or
callsign like 'SKULL%' or
callsign like 'TEAM%' or
callsign like 'VIKING%' or
callsign like 'VIKNG%' or
callsign like 'VADER%' or
callsign like 'WINK%' or
callsign like 'YANKY%'

order by date, time, callsign
