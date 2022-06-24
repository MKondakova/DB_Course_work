CREATE FUNCTION check_is_artist_update() RETURNS TRIGGER AS
$check_is_artist_update$
BEGIN
    IF NEW.is_artist = TRUE THEN
        INSERT INTO russify.artist (id) VALUES (OLD.id) ON CONFLICT DO NOTHING;
    ELSE
        RAISE EXCEPTION 'cannot delete artist';
    END IF;
    RETURN NEW;
END;
$check_is_artist_update$ LANGUAGE plpgsql;

CREATE TRIGGER check_is_artist_update
    BEFORE UPDATE OF is_artist
    ON russify.user
    FOR EACH ROW
    WHEN (OLD.is_artist IS DISTINCT FROM NEW.is_artist)
EXECUTE FUNCTION check_is_artist_update();

CREATE FUNCTION insert_to_end() RETURNS TRIGGER AS
$insert_to_end$
BEGIN
    IF EXISTS(SELECT id, next
              FROM russify.song_in_playlist
              WHERE playlist_id = NEW.playlist_id) THEN
        UPDATE russify.song_in_playlist
        SET next = NEW.id
        WHERE playlist_id = NEW.playlist_id
          AND new IS NULL;
    ELSE
        UPDATE russify.song_in_playlist
        SET is_first= TRUE
        WHERE id = new.id;
    END IF;
    RETURN new;
END;
$insert_to_end$ LANGUAGE plpgsql;

CREATE TRIGGER insert_to_end
    AFTER INSERT
    ON russify.song_in_playlist
    FOR EACH ROW
EXECUTE FUNCTION insert_to_end();

CREATE FUNCTION check_song_author() RETURNS TRIGGER AS
$check_song_author$
BEGIN
    IF (SELECT COUNT(user_id) FROM russify.song_author WHERE song_id = OLD.song_id) < 1 THEN

        RAISE EXCEPTION 'cannot delete last author';
    END IF;
    RETURN new;
END;
$check_song_author$ LANGUAGE plpgsql;

CREATE TRIGGER check_song_author
    BEFORE DELETE
    ON russify.song_author
    FOR EACH ROW
EXECUTE FUNCTION check_song_author();

CREATE FUNCTION delete_song() RETURNS TRIGGER AS
$delete_song$

BEGIN
    IF OLD.is_first THEN
        UPDATE russify.song_in_playlist
        SET is_first = TRUE
        WHERE id = OLD.next;
    ELSE
        UPDATE russify.song_in_playlist
        SET next = OLD.next
        WHERE next = OLD.id;
    END IF;

    IF EXISTS(SELECT * FROM russify.song WHERE id = OLD.song_id AND album = OLD.playlist_id) THEN
        DELETE FROM russify.song WHERE id = OLD.song_id;
    END IF;
    RETURN new;
END;
$delete_song$ LANGUAGE plpgsql;

CREATE TRIGGER delete_song
    BEFORE DELETE
    ON russify.song_in_playlist
    FOR EACH ROW
EXECUTE FUNCTION delete_song();


