CREATE FUNCTION russify.user_registered(user_id INTEGER) RETURNS bool AS
$$
SELECT EXISTS(SELECT * FROM russify.user WHERE $1 = russify.user.user_id);
$$ LANGUAGE SQL STABLE;

CREATE FUNCTION russify.is_artist(user_id INTEGER) RETURNS bool AS
$$
SELECT EXISTS(SELECT * FROM russify.user WHERE $1 = russify.user.user_id AND is_artist = TRUE);
$$ LANGUAGE SQL STABLE;

CREATE FUNCTION russify.make_artist(user_id INTEGER) RETURNS VOID AS
$$
UPDATE russify.user
SET is_artist = TRUE
WHERE $1 = russify.user.user_id
$$ LANGUAGE SQL STABLE;

CREATE FUNCTION russify.add_song(_user_id INTEGER, album INTEGER, _genre INTEGER, _title VARCHAR(50),
                                 _file VARCHAR(255),
                                 _lyrics TEXT) RETURNS VOID AS
$$
DECLARE
    _song_id INTEGER;
BEGIN
    INSERT INTO russify.song (title, file, lyrics, album, genre)
    VALUES (_title, _file, _lyrics, album, _genre)
    RETURNING id INTO _song_id;

    INSERT
    INTO russify.song_in_playlist (playlist_id, user_id, song_id)
    VALUES (album, _user_id, _song_id);

    INSERT INTO russify.song_author (song_id, user_id)
    VALUES (_song_id, _user_id);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION russify.add_song(_user_id INTEGER, album INTEGER, _genre INTEGER, _title VARCHAR(50),
                                 _file VARCHAR(255),
                                 _lyrics TEXT) RETURNS VOID AS
$$
DECLARE
    _song_id INTEGER;
BEGIN
    INSERT INTO russify.song (title, file, lyrics, album, genre)
    VALUES (_title, _file, _lyrics, album, _genre)
    RETURNING id INTO _song_id;

    INSERT
    INTO russify.song_in_playlist (playlist_id, user_id, song_id)
    VALUES (album, _user_id, _song_id);

    INSERT INTO russify.song_author (song_id, user_id)
    VALUES (_song_id, _user_id);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION russify.move_song(s_id INT, p_id INT, up bool) RETURNS VOID AS
$$
DECLARE
    b_id INT;
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

