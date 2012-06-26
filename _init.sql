delimiter $$

CREATE TABLE `about_list` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `ename` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `desc` varchar(800) COLLATE utf8_bin DEFAULT NULL,
  `minidesc` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  `area` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `team` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `img` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `pinyin` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$

delimiter $$

CREATE TABLE `all_rss` (
  `title` varchar(100) NOT NULL,
  `guid` varchar(200) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `pubdate` datetime NOT NULL,
  `country` varchar(45) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `small_cat` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `main_cat` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `editorcount2_list` (
  `id` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `guid` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `name` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `img` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `comment` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `editorcount_list` (
  `guid` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `fname` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `fcount` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `sname` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `scount` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `scomment` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `fcomment` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `img` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `editorweibo_list` (
  `name` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `wname` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `wid` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `expert_list` (
  `id` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `ename` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `address` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `location` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `company` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `phone` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `im` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bank` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `bio` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `img` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `weibo` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `blog` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `area` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `birth` datetime DEFAULT NULL,
  `bid` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `feedback_list` (
  `time` datetime NOT NULL,
  `title` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `content` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `jingyao_list` (
  `id` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `title` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `content` varchar(300) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `head_url` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `img` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `img_url` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `cat` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `mail_list` (
  `email` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `new_list` (
  `title` varchar(100) NOT NULL,
  `guid` varchar(200) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `pubdate` datetime NOT NULL,
  `country` varchar(45) NOT NULL,
  `category` varchar(100) NOT NULL,
  `small_cat` varchar(100) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `token_list` (
  `time` datetime NOT NULL,
  `token` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `expire` varchar(400) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `level` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `user_list` (
  `user` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `pwd` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `weibo_list` (
  `title` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `retweet` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  `text` varchar(400) DEFAULT NULL,
  `org_url` varchar(100) NOT NULL,
  `athur` varchar(100) DEFAULT NULL,
  `cat` varchar(100) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`org_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `wp_config` (
  `comment` int(11) NOT NULL,
  `retweet` int(11) DEFAULT NULL,
  `order` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `relation` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`comment`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `wp_list` (
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `uid` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `screen_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `cat` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `wpcheck_list` (
  `time` datetime DEFAULT NULL,
  `url` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `text` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  `retweet` int(11) DEFAULT NULL,
  `screen_name` varchar(100) NOT NULL,
  PRIMARY KEY (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$

