
-- INSERT INTO russify.user (nickname, email)
-- VALUES ('user1', 'email@uu.com'),
--        ('user2', 'email1@uu.com'),
--        ('user3', 'email2@uu.com'),
--        ('user4', 'email3@uu.com'),
--        ('user5', 'email4@uu.com');
--
-- INSERT INTO russify.user_subscription (first_user, second_user)
-- VALUES (1, 2),
--        (2, 1),
--        (2, 3),
--        (2, 4),
--        (3, 4);
-- INSERT INTO russify.playlist (title, creator)
-- VALUES ('first playlist', 1),
--        ('also first playlist', 2),
--        ('something new', 1);
-- INSERT INTO russify.playlist_subscription (member, playlist)
-- VALUES (1, 2),
--        (2, 1),
--        (2, 3);

INSERT INTO russify.genre (id, name)
VALUES (1, 'rock'),
       (2, 'pop'),
       (3, 'indie');



INSERT INTO russify.compilation(title, description)
VALUES ('first compilation', 'Этот текст так, для тестирования'),
       ('Compilation 2', 'Этот тоже, но в нем скоро появятся плейлисты, честно');
