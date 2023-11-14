--1. Find how many followers there are for “Taylor Swift”. Hint: use ARTIST_DATA.DEV.ARTISTS table

SELECT ARTIST, FOLLOWERS FROM ARTIST_DATA.DEV.ARTISTS
WHERE ARTIST = 'Taylor Swift';

---------------------------------------------
--2. Find all male “hip hop” artists who have followers between 2,000,000 to 1,000,000. Hint: use ARTIST_DATA.DEV.ARTISTS table

SELECT ARTIST, GENRES, GENDER
FROM ARTIST_DATA.DEV.ARTISTS
WHERE GENDER = 'M'
AND FOLLOWERS BETWEEN 1000000 AND 2000000
AND GENRES LIKE '%hip hop%';

---------------------------------------------
-- 3. Find top 3 song_name for  “Taylor Swift” based on popularity.

SELECT gs.SONG_NAME, gs.ARTIST, gs.id, p.id, p.artist, p.song_name, p.popularity
FROM GRAMMY_SONGS gs
JOIN SONG_ATTRIBUTES p ON gs.ARTIST = p.ARTIST AND gs.SONG_NAME = p.SONG_NAME
WHERE gs.ARTIST = 'Taylor Swift'
ORDER BY p.POPULARITY DESC
LIMIT 3;
---------------------------------------------
--4. Find top 3 “modern country rock” genre song names based on their popularity. Hint: join 2 tables

SELECT s.SONG_NAME, a.GENRE, s.popularity, s.artist
FROM SONG_ATTRIBUTES s
JOIN GRAMMY_ALBUMS a ON s.album = a.album AND s.artist = a.artist
WHERE a.GENRE IN ('Modern', 'Rock', 'Country')
ORDER BY s.POPULARITY DESC
LIMIT 3;

---------------------------------------------
--5. Select 3 GRAMMY_SONGS names in format: “song_name by artist_name (year)”. Hint use string functions

SELECT CONCAT(SONG_NAME, ' by ', ARTIST, ' (', GRAMMY_YEAR, ')') AS FORMATTED_SONG
FROM GRAMMY_SONGS
LIMIT 3;

---------------------------------------------
--6. Select a unique list of labels grouped by artist names in (WIZ KHALIFA, TAYLOR SWIFT, DRAKE, CHRIS BROWN) . Hint: use aggregate functions

SELECT ARTIST, LISTAGG(DISTINCT LABEL, ', ') WITHIN GROUP (ORDER BY LABEL) AS unique_labels
FROM ARTIST_DATA.DEV.ALBUM_LABEL
WHERE ARTIST IN ('WIZ KHALIFA', 'TAYLOR SWIFT', 'DRAKE', 'CHRIS BROWN')
GROUP BY ARTIST;

---------------------------------------------
--7. Show what percentage of total revenue is from streaming for all artists. Hint: use ARTIST_DATA.DEV.MONEY_MAKERS table with Numeric functions . Percentage = (streaming/total)* 100

SELECT ARTIST, TO_VARIANT(ROUND((SUM(STREAMING) / SUM(TOTAL)) * 100, 2)) || '%' AS percentage_of_total_revenue
FROM ARTIST_DATA.DEV.MONEY_MAKERS
GROUP BY ARTIST;

---------------------------------------------
--8. Create a view in snowflake which shows GRAMMY_SONGS + SONG_ATTRIBUTES for those songs.

CREATE OR REPLACE VIEW GRAMMY_SONGS_WITH_ATTRIBUTES AS
SELECT gs.ID AS gs_ID, 
gs.SONG_NAME AS gs_SONGNAME, 
gs.ARTIST AS gs_ARTIST, 
sa.ARTIST AS sa_ARTIST,
sa.ID AS sa_ID, 
sa.SONG_NAME, 
sa.DANCEABILITY
FROM GRAMMY_SONGS gs
JOIN SONG_ATTRIBUTES sa
ON gs.SONG_NAME = sa.SONG_NAME AND gs.artist = sa.artist;


SELECT * FROM GRAMMY_SONGS_WITH_ATTRIBUTES;

---------------------------------------------
--9.  Insert relevant and good data into GRAMMY_SONGS from ARTIST_DATA.DEV.NEW_GRAMMY_DATA table . Hint: this requires data conversion and INSERT from SELECT.

INSERT INTO ARTIST_DATA.DEV.GRAMMY_SONGS (ARTIST, GRAMMY_YEAR, AWARD, SONG_NAME)
SELECT ARTIST, YEAR, CATEGORY, NOMINEE
FROM NEW_GRAMMY_DATA
WHERE WINNER = true;

---------------------------------------------

SELECT * FROM ARTISTS;
SELECT * FROM ALBUM_LABEL;
SELECT * FROM GRAMMY_SONGS;
SELECT * FROM GRAMMY_ALBUMS;
SELECT * FROM NEW_GRAMMY_DATA;
SELECT * FROM MONEY_MAKERS;
SELECT * FROM SONG_ATTRIBUTES;