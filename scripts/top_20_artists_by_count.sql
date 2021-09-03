SELECT
	artist.name, COUNT(*), COUNT(*) * 100.0 / (SELECT COUNT(*) FROM track) AS percentage
FROM
	artistry
	INNER JOIN track ON artistry.track_id = track.id
	INNER JOIN artist ON artistry.artist_id = artist.id
GROUP BY artist.id
ORDER BY COUNT(*) DESC
LIMIT 20;
