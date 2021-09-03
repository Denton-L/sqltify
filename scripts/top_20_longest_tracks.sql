SELECT
	track.title, GROUP_CONCAT(artist.name), CAST(track.duration_ms as FLOAT) / 1000 / 60 AS minutes
FROM
	artistry
	INNER JOIN track ON artistry.track_id = track.id
	INNER JOIN artist ON artistry.artist_id = artist.id
GROUP BY track.id
ORDER BY minutes DESC
LIMIT 20;
