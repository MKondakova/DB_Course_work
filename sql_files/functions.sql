CREATE FUNCTION russify.user_registered(user_id INTEGER)
    RETURNS TABLE
                (
                    nickname VARCHAR(100),
                    is_artist BOOLEAN
                )
AS
$$
SELECT nickname, is_artist
  FROM russify.user
 WHERE $1 = russify.user.user_id;
$$ LANGUAGE sql
STABLE;

CREATE FUNCTION russify.is_artist(user_id INTEGER) RETURNS bool AS
$$
SELECT EXISTS(SELECT * FROM russify.user WHERE $1 = russify.user.user_id AND is_artist = TRUE);
$$ LANGUAGE sql
STABLE;

CREATE FUNCTION russify.make_artist(user_id INTEGER) RETURNS VOID AS
$$
UPDATE russify.user
   SET is_artist = TRUE
 WHERE $1 = russify.user.user_id
$$ LANGUAGE sql
VOLATILE;

CREATE FUNCTION russify.add_song(_user_id INTEGER, album INTEGER, _genre INTEGER, _title VARCHAR(50),
                                 _file VARCHAR(255),
                                 _lyrics TEXT) RETURNS VOID AS
$$
DECLARE
    _song_id INTEGER;
BEGIN
       INSERT INTO russify.song (title, file, lyrics, album, genre)
       VALUES ($4, $5, $6, $2, $3)
    RETURNING id INTO _song_id;

    INSERT INTO russify.song_in_playlist (playlist_id, user_id, song_id) VALUES (album, _user_id, _song_id);

    INSERT INTO russify.song_author (song_id, user_id) VALUES (_song_id, _user_id);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION russify.move_song(s_id INT, p_id INT, up bool) RETURNS VOID AS
$$
BEGIN
    IF up THEN
        -- c a b; b moves up

          WITH b AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id)
        UPDATE russify.song_in_playlist
           SET next = b.next
         WHERE next = b.id;

          WITH b AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id),
               a AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND next = b.next AND song_id != s_id)
        UPDATE russify.song_in_playlist
           SET next = a.id
         WHERE id = b.id;

          WITH b AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id)
        UPDATE russify.song_in_playlist
           SET next = b.id
         WHERE next = b.next
           AND song_id != s_id;
    ELSE
        -- c a b; a moves down

          WITH a AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id),
               c AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND next = a.id)
        UPDATE russify.song_in_playlist
           SET next = a.next
         WHERE id = c.id;

          WITH a AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id),
               b AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND id = a.next)
        UPDATE russify.song_in_playlist
           SET next = b.next
         WHERE id = a.id;

          WITH a AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND song_id = s_id),
               b AS (SELECT * FROM song_in_playlist WHERE playlist_id = p_id AND next = a.next AND song_id != s_id)
        UPDATE russify.song_in_playlist
           SET next = a.id
         WHERE id = b.id;

    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION russify.get_playlists(user_id INTEGER)
    RETURNS TABLE
                (
                    id INT,
                    title VARCHAR(50),
                    is_private BOOLEAN,
                    is_collaborative BOOLEAN,
                    creator int,

                    cover VARCHAR(255),
                    description TEXT,
                    is_album bool
                )
AS
$$
SELECT id, title, is_private, is_collaborative, creator, cover, description, is_album
  FROM russify.playlist
 WHERE creator = user_id
   AND is_album = FALSE
$$ LANGUAGE sql
STABLE;

CREATE FUNCTION russify.get_albums(user_id INTEGER)
    RETURNS TABLE
                (
                    id INT,
                    title VARCHAR(50),
                    is_private BOOLEAN,
                    is_collaborative BOOLEAN,
                    creator int,
                    cover VARCHAR(255),
                    description TEXT,
                    is_album bool
                )
AS
$$
SELECT id, title, is_private, is_collaborative, creator, cover, description, is_album
  FROM russify.playlist
 WHERE creator = user_id
   AND is_album = TRUE
$$ LANGUAGE sql
STABLE;

CREATE FUNCTION russify.get_songs(playlist_id INTEGER)
    RETURNS TABLE
                (
                    id int,
                    is_first BOOLEAN,
                    next int,
                    title VARCHAR(50),
                    file VARCHAR(255),
                    genre VARCHAR(100)
                )
AS
$$
SELECT song_in_playlist.id, is_first, next, title, file, name
  FROM russify.song_in_playlist
           LEFT JOIN russify.song s
           ON s.id = song_in_playlist.song_id
           LEFT JOIN russify.genre g
           ON s.genre = g.id
 WHERE song_in_playlist.playlist_id = $1
$$ LANGUAGE sql
STABLE;

CREATE FUNCTION russify.find_songs(_title varchar(50))
    RETURNS TABLE
                (
                    id int,
                    title VARCHAR(50),
                    file VARCHAR(255)
                )
AS
$$
SELECT id, title, file
  FROM russify.song
 WHERE russify.make_title_tsvector(title) @@ phraseto_tsquery($1)
 LIMIT 10;
$$ LANGUAGE sql
STABLE;

