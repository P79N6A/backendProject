CREATE TABLE `t_categorys` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_status` (
  `status_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `t_tags` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `t_user_videos` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL DEFAULT '0' COMMENT '用户id',
  `video_id` varchar(16) NOT NULL DEFAULT '0' COMMENT '视频资源f_id',
  PRIMARY KEY (`f_id`),
  KEY `unique` (`user_id`,`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_users` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `profile` varchar(255) NOT NULL DEFAULT '',
  `user_id` varchar(255) NOT NULL DEFAULT '0' COMMENT '用户id',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_video_categorys` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` varchar(16) NOT NULL DEFAULT '0',
  `category` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`f_id`),
  KEY `unique` (`video_id`,`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `t_video_tags` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` varchar(16) NOT NULL DEFAULT '0',
  `tag` varchar(255) NOT NULL DEFAULT '0',
  PRIMARY KEY (`f_id`),
  KEY `unique` (`video_id`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `t_videos` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `h_id` varchar(16) DEFAULT '0' COMMENT '视频hash id md5',
  `name` varchar(255) NOT NULL DEFAULT '',
  `en_name` varchar(255) NOT NULL DEFAULT '',
  `res_url` varchar(255) DEFAULT NULL COMMENT '资源url',
  `definition` varchar(128) NOT NULL DEFAULT '0' COMMENT '清晰度',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_billboard` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `qr_url` varchar(255) NOT NULL DEFAULT '',
  `notice` varchar(255) NOT NULL DEFAULT '',
  `modify_user` varchar(255) NOT NULL DEFAULT '',
  `modify_time` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
