--1. Find how many followers there are for “Taylor Swift”. Hint: use ARTIST_DATA.DEV.ARTISTS table
SELECT "ARTIST", "FOLLOWERS" FROM "ARTIST_DATA"."DEV"."ARTISTS"
WHERE "ARTIST" = 'Taylor Swift';

---------------------------------------------
--2. Find all male “hip hop” artists who have followers between 2,000,000 to 1,000,000. Hint: use ARTIST_DATA.DEV.ARTISTS table
SELECT ARTIST, GENRES, GENDER
FROM ARTIST_DATA.DEV.ARTISTS
WHERE GENDER = 'M'
AND FOLLOWERS BETWEEN 1000000 AND 2000000
AND GENRES LIKE '%hip hop%';

---------------------------------------------
-- 3. Find top 3 song_name for  “Taylor Swift” based on popularity.
SELECT SONG_NAME, ARTIST, GRAMMY_YEAR, AWARD
FROM GRAMMY_SONGS
WHERE ARTIST = 'Taylor Swift'
ORDER BY AWARD DESC
LIMIT 3;

---------------------------------------------
--4. Find top 3 “modern country rock” genre song names based on their popularity. Hint: join 2 tables
SELECT s.SONG_NAME, a.GENRE
FROM GRAMMY_SONGS s
JOIN GRAMMY_ALBUMS a ON s.ID = a.ID
WHERE a.GENRE IN ('Modern', 'Rock', 'Country')
ORDER BY s.AWARD DESC
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
--Error: invalid identifier 'LABEL' (line 33)
---------------------------------------------
--7. Show what percentage of total revenue is from streaming for all artists. Hint: use ARTIST_DATA.DEV.MONEY_MAKERS table with Numeric functions . Percentage = (streaming/total)* 100
SELECT SUM(STREAMING) AS total_streaming_revenue,
SUM(TOTAL) AS total_revenue,
(SUM(STREAMING) / SUM(TOTAL)) * 100 AS percentage_of_total_revenue
FROM ARTIST_DATA.DEV.MONEY_MAKERS;

---------------------------------------------
--8. Create a view in snowflake which shows GRAMMY_SONGS + SONG_ATTRIBUTES for those songs.

CREATE VIEW GRAMMY_SONGS_WITH_ATTRIBUTES AS
SELECT gs.ID AS gs_ID,
gs.SONG_NAME AS gs_SongName,
gs.ARTIST AS gs_Artist,
sa.ID AS sa_ID
FROM GRAMMY_SONGS gs
JOIN SONG_ATTRIBUTES sa
ON gs.ID = sa.ID;


SELECT * FROM GRAMMY_SONGS_WITH_ATTRIBUTES;
--SQL COMPILATION ERROR : ID

---------------------------------------------
--9.  Insert relevant and good data into GRAMMY_SONGS from ARTIST_DATA.DEV.NEW_GRAMMY_DATA table . Hint: this requires data conversion and INSERT from SELECT.

INSERT INTO ARTIST_DATA.DEV.GRAMMY_SONGS (ARTIST, GRAMMY_YEAR)
SELECT ARTIST, YEAR
FROM NEW_GRAMMY_DATA
---------------------------------------------


SELECT * FROM ARTISTS;
SELECT * FROM ARTIST_DATA.DEV.ALBUM_LABEL;
SELECT * FROM GRAMMY_SONGS;
SELECT * FROM GRAMMY_ALBUMS;
SELECT * FROM NEW_GRAMMY_DATA;
SELECT * FROM MONEY_MAKERS;
SELECT * FROM ARTIST_DATA.DEV.SONG_ATTRIBUTES;

