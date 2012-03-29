delimiter $$

CREATE TABLE `all_rss` (
  `title` varchar(100) CHARACTER SET latin1 NOT NULL,
  `description` varchar(1000) CHARACTER SET latin1 DEFAULT NULL,
  `guid` varchar(200) CHARACTER SET latin1 DEFAULT NULL,
  `pubdate` datetime DEFAULT NULL,
  `country` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

delimiter $$

CREATE TABLE `editor_list` (
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `company` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `birthday` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `phone` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `weibo` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `blog` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

delimiter $$

CREATE TABLE `mail_list` (
  `email` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `country` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `id` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

delimiter $$

CREATE TABLE `new_list` (
  `title` varchar(100) NOT NULL,
  `guid` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `pubdate` datetime DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1$$

delimiter $$

CREATE TABLE `token_list` (
  `time` datetime NOT NULL,
  `token` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `expire` varchar(400) COLLATE utf8_bin DEFAULT NULL,
  `type` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

delimiter $$

CREATE TABLE `weibo_list` (
  `title` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `url` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `retweet` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  `text` varchar(400) CHARACTER SET latin1 DEFAULT NULL,
  `org_url` varchar(100) CHARACTER SET latin1 NOT NULL,
  `athur` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `cat` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`org_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

