from users.connectors.snowflake import connection


class SnowflakeModel:

    def __init__(self):
        connection.execute("USE WAREHOUSE COMPUTE_WH")
    
    def get_followers_by_user(self, user):
        followers_query = "SELECT FOLLOWERS FROM ARTIST_DATA.DEV.ARTISTS WHERE ARTIST = %s"
        labels_query = """
            SELECT ARTIST, LISTAGG(DISTINCT LABEL, ', ') WITHIN GROUP (ORDER BY LABEL) AS unique_labels
            FROM ARTIST_DATA.DEV.ALBUM_LABEL
            WHERE ARTIST = %s GROUP BY ARTIST;
        """

        followers = connection.execute(followers_query, (user,)).fetchone()
        labels = connection.execute(labels_query, (user.upper(),)).fetchone()
        return followers, labels
    
    def get_awards_by_id(self, id):
        awards_query = f"""SELECT AWARD as award, GRAMMY_YEAR as year, SONG_NAME as song FROM GRAMMY_SONGS WHERE ARTIST IN (SELECT ARTIST FROM ARTISTS WHERE ID={id}) AND AWARD IS NOT NULL
                        UNION
                        SELECT AWARD as award, GRAMMY_YEAR as year, ALBUM as song FROM GRAMMY_ALBUMS WHERE ARTIST IN (SELECT ARTIST FROM ARTISTS WHERE ID={id}) AND AWARD IS NOT NULL;"""

        awards = connection.execute(awards_query).fetchall()
        lst = []
        for x in awards:
            # this would not be required with DictCursor
            inner_obj = {}
            inner_obj['award'] = x[0]
            inner_obj['year'] = x[1]
            inner_obj['album_song'] = x[2]
            lst.append(inner_obj)
        return lst
