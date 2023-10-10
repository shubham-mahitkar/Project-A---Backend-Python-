from users.connectors.snowflake import connection
from users.utils import util

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
            inner_obj = {}
            inner_obj['award'] = x[0]
            inner_obj['year'] = x[1]
            inner_obj['album_song'] = x[2]
            lst.append(inner_obj)
        return lst

    def get_max_id(self, table):
        sql = f"SELECT MAX(id) AS max_id FROM ARTIST_DATA.DEV.{table};"
        result = connection.execute(sql).fetchone()
        return result[0] + 1 if result[0] is not None else 1

    def insert_into_artists(self, artist_name, number_of_followers, genre, NumAlbums, YearFirstAlbum, Gender, Group_or_Solo):
        iid = self.get_max_id("ARTISTS")
        sql = f"INSERT INTO ARTIST_DATA.DEV.ARTISTS (ID, ARTIST, FOLLOWERS, GENRES, NUM_ALBUMS, YEAR_FIRST_ALBUM, GENDER, GROUP_SOLO) " \
            f"VALUES ('{iid}', '{artist_name}', '{number_of_followers}', '{genre}', '{NumAlbums}', '{YearFirstAlbum}', '{Gender}', '{Group_or_Solo}')"
        connection.execute(sql)

    def insert_into_album_label(self, artist_name, labels):
        iid = self.get_max_id("ALBUM_LABEL")
        sql = f"INSERT INTO ARTIST_DATA.DEV.ALBUM_LABEL (ID, ARTIST, LABEL) " \
            f"VALUES ('{iid}', '{artist_name}', '{labels}')"
        connection.execute(sql)

    def snowflake_insert_bulk_users(self, csv_data):
        try:
            headers = next(csv_data)
            for row in csv_data:
                artist_name, email, access_to_application, followers_str, labels, genre, NumAlbums, YearFirstAlbum, Gender, Group_or_Solo = row[:10]
                number_of_followers = util.convert_numeric_string(followers_str).replace(',', '')

                self.insert_into_artists(artist_name, number_of_followers, genre, NumAlbums, YearFirstAlbum, Gender, Group_or_Solo)
                self.insert_into_album_label(artist_name, labels)

        except Exception as e:
            print(e)