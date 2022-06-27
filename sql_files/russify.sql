CREATE SCHEMA russify;

CREATE TABLE russify.user
    (user_id INTEGER
         PRIMARY KEY,
     nickname VARCHAR(100) NOT NULL,
     is_artist BOOLEAN NOT NULL DEFAULT FALSE,
     avatar VARCHAR(255) NULL
    );

CREATE TABLE russify.artist
    (id INTEGER
         PRIMARY KEY
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT,
     about TEXT NULL,
     additional_photo VARCHAR(255) NULL
    );

CREATE TABLE russify.user_subscription
    (id SERIAL
         PRIMARY KEY,
     first_user INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     second_user INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     UNIQUE (first_user, second_user)

    );

CREATE INDEX user_subscription_idx ON russify.user_subscription (first_user, second_user);

CREATE TABLE russify.playlist
    (id SERIAL
         PRIMARY KEY,
     title VARCHAR(50) NOT NULL,
     creator INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     description VARCHAR(300) NULL,
     cover VARCHAR(200) NULL,
     is_album BOOLEAN NOT NULL DEFAULT FALSE,
     is_private BOOLEAN NOT NULL DEFAULT TRUE,
     is_collaborative BOOLEAN NOT NULL DEFAULT FALSE
    );

CREATE INDEX playlist_idx ON russify.playlist (creator);

CREATE TABLE russify.playlist_subscription
    (id SERIAL
         PRIMARY KEY,
     member INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     playlist INTEGER
         REFERENCES russify.playlist ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL NOT NULL,
     UNIQUE (member, playlist)

    );

CREATE INDEX playlist_subscription_idx ON russify.playlist_subscription (member);

CREATE TABLE russify.genre
    (id INTEGER
         PRIMARY KEY,
     name VARCHAR(100) NOT NULL
         UNIQUE
    );

CREATE TABLE russify.song
    (id SERIAL
         PRIMARY KEY,
     title VARCHAR(50) NOT NULL,
     file VARCHAR(255)
         UNIQUE NOT NULL,
     lyrics TEXT NULL,
     album INTEGER
         REFERENCES russify.playlist ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     genre INTEGER
         REFERENCES russify.genre ON DELETE SET NULL ON UPDATE RESTRICT NULL
    );

CREATE FUNCTION russify.make_title_tsvector(title TEXT) RETURNS tsvector AS
$$
BEGIN
    RETURN TO_TSVECTOR('russian', title) || TO_TSVECTOR('english', title);
END
$$ LANGUAGE 'plpgsql'
IMMUTABLE;

CREATE INDEX song_idx ON russify.song USING gin (russify.make_title_tsvector(title));

CREATE TABLE russify.song_author
    (id SERIAL
         PRIMARY KEY,
     song_id INTEGER
         REFERENCES russify.song ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     user_id INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     UNIQUE (song_id, user_id)
    );

CREATE TABLE russify.album_author
    (id SERIAL
         PRIMARY KEY,
     user_id INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     playlist_id INTEGER
         REFERENCES russify.playlist ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     UNIQUE (playlist_id, user_id)

    );

CREATE TABLE russify.song_in_playlist
    (id SERIAL
         PRIMARY KEY,
     playlist_id INTEGER
         REFERENCES russify.playlist ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     is_first BOOLEAN NOT NULL DEFAULT FALSE,
     next INTEGER
         REFERENCES russify.song_in_playlist NULL,
     user_id INTEGER
         REFERENCES russify.user ON DELETE RESTRICT ON UPDATE RESTRICT NOT NULL,
     song_id INTEGER
         REFERENCES russify.song ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     UNIQUE (playlist_id, song_id)
    );

CREATE INDEX song_in_playlist_idx ON russify.song_in_playlist (playlist_id);
CREATE TABLE russify.compilation
    (id SERIAL
         PRIMARY KEY,
     title VARCHAR(50) NOT NULL,
     description VARCHAR(300) NOT NULL
    );

CREATE TABLE russify.playlist_in_compilation
    (id SERIAL
         PRIMARY KEY,
     compilation_id INTEGER
         REFERENCES russify.compilation ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     playlist_id INTEGER
         REFERENCES russify.playlist ON DELETE CASCADE ON UPDATE RESTRICT NOT NULL,
     UNIQUE (compilation_id, playlist_id)
    );

CREATE ROLE authenticator NOINHERIT LOGIN PASSWORD 'mysecretpassword';
GRANT USAGE ON SCHEMA russify TO authenticator;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA russify TO authenticator;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA russify TO authenticator;
