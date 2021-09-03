SELECT
	artist.name, SUM(duration_ms) / 1000.0 / 60 / 60 AS hours
FROM
	artistry
	INNER JOIN track ON artistry.track_id = track.id
	INNER JOIN artist ON artistry.artist_id = artist.id
GROUP BY artist.id
ORDER BY hours DESC
LIMIT 20;
