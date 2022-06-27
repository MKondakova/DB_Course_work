CREATE FUNCTION russify.check_is_artist_update() RETURNS TRIGGER AS
$check_is_artist_update$
BEGIN
    IF new.is_artist = TRUE THEN
        INSERT INTO russify.artist (id) VALUES (old.user_id) ON CONFLICT DO NOTHING;
    ELSE
        RAISE EXCEPTION 'cannot delete artist';
    END IF;
    RETURN new;
END;
$check_is_artist_update$ LANGUAGE plpgsql;

CREATE TRIGGER check_is_artist_update
    BEFORE UPDATE OF is_artist
    ON russify.user
    FOR EACH ROW
    WHEN (old.is_artist IS DISTINCT FROM new.is_artist)
EXECUTE FUNCTION russify.check_is_artist_update();

CREATE FUNCTION russify.insert_to_end() RETURNS TRIGGER AS
$insert_to_end$
BEGIN
    IF (SELECT COUNT(*) > 1
          FROM (SELECT id, next FROM russify.song_in_playlist WHERE playlist_id = new.playlist_id) AS "in") THEN
        UPDATE russify.song_in_playlist SET next = new.id WHERE playlist_id = new.playlist_id AND new IS NULL;
    ELSE
        UPDATE russify.song_in_playlist SET is_first= TRUE WHERE id = new.id;
    END IF;
    RETURN new;
END;
$insert_to_end$ LANGUAGE plpgsql;

CREATE TRIGGER insert_to_end
    AFTER INSERT
    ON russify.song_in_playlist
    FOR EACH ROW
EXECUTE FUNCTION russify.insert_to_end();

CREATE FUNCTION russify.check_song_author() RETURNS TRIGGER AS
$check_song_author$
BEGIN
    IF (SELECT COUNT(user_id) FROM russify.song_author WHERE song_id = old.song_id) < 1 THEN

        RAISE EXCEPTION 'cannot delete last author';
    END IF;
    RETURN new;
END;
$check_song_author$ LANGUAGE plpgsql;

CREATE TRIGGER check_song_author
    BEFORE DELETE
    ON russify.song_author
    FOR EACH ROW
EXECUTE FUNCTION russify.check_song_author();

CREATE FUNCTION russify.delete_song() RETURNS TRIGGER AS
$delete_song$

BEGIN
    IF old.is_first THEN
        UPDATE russify.song_in_playlist SET is_first = TRUE WHERE id = old.next;
    ELSE
        UPDATE russify.song_in_playlist SET next = old.next WHERE next = old.id;
    END IF;

    IF EXISTS(SELECT * FROM russify.song WHERE id = old.song_id AND album = old.playlist_id) THEN
        DELETE FROM russify.song WHERE id = old.song_id;
    END IF;
    RETURN new;
END;
$delete_song$ LANGUAGE plpgsql;

CREATE TRIGGER delete_song
    BEFORE DELETE
    ON russify.song_in_playlist
    FOR EACH ROW
EXECUTE FUNCTION russify.delete_song();


