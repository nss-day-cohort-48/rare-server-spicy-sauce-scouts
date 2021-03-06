CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);


INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');



INSERT INTO `Categories` ('label') VALUES ('News');
INSERT INTO `Tags` ('label') VALUES ('JavaScript');
INSERT INTO `Reactions` ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO `Users` VALUES (null, 'Test', 'Name', 'test@email.com', 'I was created as a test', 'test_dummy123', 'password', 
'https://devforum.roblox.com/uploads/default/original/4X/2/d/a/2dafbedd0c9b7995743afce8ad87e2d3df15ec21.jpeg', '12/08/1999', 'TRUE');
INSERT INTO `Users` VALUES (null, 'Fake', 'Guy', 'fake@email.com', 'I am a fake guy', 'fake_guy456', 'password', 
'https://www.smashbros.com/assets_v2/img/fighter/steve/main.png', '12/08/1999', 'TRUE');

INSERT INTO `Subscriptions` VALUES (null, 1, 2, "06/07/2008");
INSERT INTO `Subscriptions` VALUES (null, 2, 1, "06/07/2008");

INSERT INTO `Posts` VALUES (null, 1, 1, 'Test Post 1', '11/08/2000', 
'https://bbts1.azureedge.net/images/p/full/2020/03/8e4048c4-6f34-49af-9498-26e1bb34fe5d.jpg', 'This is a test post', 'TRUE');
INSERT INTO `Posts` VALUES (null, 2, 1, 'Fake Post LOL', '06/06/2006', 
'https://twinfinite.net/wp-content/uploads/2020/10/Screen-Shot-2020-10-13-at-11.47.43-AM.jpg', 'MUNCRUFT', 'TRUE');

INSERT INTO `Comments` VALUES (null, 1, 2, 'Nice Post');
INSERT INTO `Comments` VALUES (null, 1, 2, 'Even Nicer Post');
INSERT INTO `Comments` VALUES (null, 2, 1, 'Git Gud');

INSERT INTO `Reactions` VALUES (null, 'Fire', 'https://i.pinimg.com/originals/e9/3a/6e/e93a6e90e2f5d302cba9cc870f2fbe42.png');

INSERT INTO `PostReactions` VALUES (null, 1, 4, 2);
INSERT INTO `PostReactions` VALUES (null, 2, 3, 2);
INSERT INTO `PostReactions` VALUES (null, 3, 1, 3);

INSERT INTO `Tags` VALUES (null, 'Crafting');

INSERT INTO `PostTags` VALUES (null, 1, 1);
INSERT INTO `PostTags` VALUES (null, 2, 4);
INSERT INTO `PostTags` VALUES (null, 2, 2);

INSERT INTO `Categories` VALUES (null, 'Blocks');

SELECT * FROM `Categories`;


SELECT
  pt.id,
  pt.tag_id,
  pt.post_id,
  t.id,
  t.label,
  p.id,
  p.user_id
FROM PostTags pt
JOIN Tags t
  on t.id = pt.tag_id
JOIN Posts p
  on p.id = pt.post_id
WHERE pt.post_id = 1

SELECT
  pt.id,
  pt.tag_id,
  pt.post_id,
  t.id,
  t.label,
  p.id,
  p.user_id
FROM PostTags pt
JOIN Tags t
  on t.id = pt.tag_id
JOIN Posts p
  on p.id = pt.post_id
WHERE p.user_id = 2

SELECT * FROM PostTags

SELECT * FROM Tags

SELECT * FROM Posts

SELECT
  t.id,
  t.label,
  pt.tag_id,
  pt.post_id,
  p.id,
  p.content
FROM Tags t
JOIN PostTags pt
  on pt.tag_id = t.id
JOIN Posts p
  on p.id = pt.post_id
WHERE post_id = 2

SELECT *
FROM users

SELECT *
FROM Posts

SELECT *
FROM Comments
WHERE post_id = 1

SELECT
  pt.id,
  pt.post_id,
  pt.tag_id,
  p.id,
  p.user_id,
  p.category_id,
  p.title,
  p.publication_date,
  p.image_url,
  p.content,
  p.approved,
  t.id,
  t.label
FROM PostTags pt
LEFT JOIN Posts p
    on p.id = pt.post_id
JOIN Tags t
    on t.id = pt.tag_id