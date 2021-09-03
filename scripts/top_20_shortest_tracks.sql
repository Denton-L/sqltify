SELECT
	track.title, GROUP_CONCAT(artist.name), CAST(track.duration_ms as FLOAT) / 1000 AS seconds
FROM
	artistry
	INNER JOIN track ON artistry.track_id = track.id
	INNER JOIN artist ON artistry.artist_id = artist.id
GROUP BY track.id
ORDER BY seconds ASC
LIMIT 20;
