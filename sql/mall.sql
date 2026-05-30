-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: mall
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_address`
--

DROP TABLE IF EXISTS `t_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '外键',
  `consignee` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '收货人姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '联系方式',
  `province` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省',
  `city` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市',
  `area` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区',
  `street` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '街道',
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '详细地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_address`
--

LOCK TABLES `t_address` WRITE;
/*!40000 ALTER TABLE `t_address` DISABLE KEYS */;
INSERT INTO `t_address` VALUES (0,9,'小明','18132221182','河北','石家庄','高新区','天山大街','高新区天山大街186号  眼科医院宿舍'),(1,9,'小明','18132221182','河北','石家庄','裕华区','裕华路','裕华路天山海世界3楼'),(2,10,'小红','18812345678','北京','北京','朝阳区','东三环辅路','东三环辅路中央电视台5楼');
/*!40000 ALTER TABLE `t_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_admin`
--

DROP TABLE IF EXISTS `t_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `level_id` int DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `id_card` varchar(45) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `register_time` timestamp NULL DEFAULT NULL,
  `last_active_time` timestamp NULL DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_admin`
--

LOCK TABLES `t_admin` WRITE;
/*!40000 ALTER TABLE `t_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_balance`
--

DROP TABLE IF EXISTS `t_balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_balance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '外键',
  `change` int NOT NULL DEFAULT '0' COMMENT '变动金额',
  `balance` int NOT NULL COMMENT '余额',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '类型',
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '详细描述',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账户余额表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_balance`
--

LOCK TABLES `t_balance` WRITE;
/*!40000 ALTER TABLE `t_balance` DISABLE KEYS */;
INSERT INTO `t_balance` VALUES (1,9,0,100000,'未知字段','小明的余额','2023-02-13 22:15:02'),(2,10,0,200000,'未知字段','小红的余额','2023-02-13 22:15:02');
/*!40000 ALTER TABLE `t_balance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_balance_lock`
--

DROP TABLE IF EXISTS `t_balance_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_balance_lock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '外键',
  `change` int NOT NULL DEFAULT '0' COMMENT '变动',
  `lock_balance` int NOT NULL COMMENT '锁定余额',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型',
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '描述',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账户锁定余额表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_balance_lock`
--

LOCK TABLES `t_balance_lock` WRITE;
/*!40000 ALTER TABLE `t_balance_lock` DISABLE KEYS */;
INSERT INTO `t_balance_lock` VALUES (1,9,0,500,'未知字段','小明的账户锁定额','2023-02-13 22:15:02'),(2,10,0,1000,'未知字段','小红的账户锁定额','2023-02-13 22:15:02');
/*!40000 ALTER TABLE `t_balance_lock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_cart`
--

DROP TABLE IF EXISTS `t_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '用户编号',
  `good_id` int DEFAULT NULL COMMENT '商品编号',
  `number` int DEFAULT NULL COMMENT '购买数量',
  `creat_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='购物车表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_cart`
--

LOCK TABLES `t_cart` WRITE;
/*!40000 ALTER TABLE `t_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_category`
--

DROP TABLE IF EXISTS `t_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL,
  `parent_category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_category`
--

LOCK TABLES `t_category` WRITE;
/*!40000 ALTER TABLE `t_category` DISABLE KEYS */;
INSERT INTO `t_category` VALUES (1,'百货',NULL),(2,'美食',NULL),(3,'美妆',NULL);
/*!40000 ALTER TABLE `t_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_coin`
--

DROP TABLE IF EXISTS `t_coin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_coin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '外键',
  `change` int NOT NULL DEFAULT '0' COMMENT '变动',
  `coin` int NOT NULL COMMENT '积分',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型',
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '详细',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_coin`
--

LOCK TABLES `t_coin` WRITE;
/*!40000 ALTER TABLE `t_coin` DISABLE KEYS */;
INSERT INTO `t_coin` VALUES (1,9,0,100,'未知字段','小明的积分','2023-02-13 22:15:02'),(2,10,0,0,'未知字段','小红的积分','2023-02-13 22:15:02');
/*!40000 ALTER TABLE `t_coin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_delivery_rule`
--

DROP TABLE IF EXISTS `t_delivery_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_delivery_rule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `good_id` int DEFAULT NULL COMMENT '商品id',
  `spec_id` int DEFAULT NULL COMMENT '规格id',
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省',
  `city` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '市',
  `area` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '区',
  `is_reachable` tinyint(1) DEFAULT NULL COMMENT '是否可抵达    0：不可抵达     1：可抵达',
  `delivery_fee` int DEFAULT '0' COMMENT '邮寄费用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_delivery_rule`
--

LOCK TABLES `t_delivery_rule` WRITE;
/*!40000 ALTER TABLE `t_delivery_rule` DISABLE KEYS */;
INSERT INTO `t_delivery_rule` VALUES (22,30,NULL,'1003',NULL,NULL,0,11),(23,30,NULL,'1004',NULL,NULL,0,11),(24,36,0,'河东','string','string',0,10000),(25,37,0,'河西','string','string',0,10000),(26,38,NULL,'光耦的那个','string','string',0,10000),(39,53,NULL,'string',NULL,NULL,0,0),(40,54,NULL,'string',NULL,NULL,0,0),(41,55,NULL,'string',NULL,NULL,0,0),(42,56,NULL,'string',NULL,NULL,0,0),(43,59,NULL,'string',NULL,NULL,0,0),(44,60,NULL,'string',NULL,NULL,0,0),(45,61,NULL,'string',NULL,NULL,0,0),(46,62,NULL,'string',NULL,NULL,0,0),(47,63,NULL,'string',NULL,NULL,0,0);
/*!40000 ALTER TABLE `t_delivery_rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_flash_order`
--

DROP TABLE IF EXISTS `t_flash_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_flash_order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `package_id` int DEFAULT NULL COMMENT '包id',
  `status` tinyint NOT NULL COMMENT '状态   0：未付款    1：已付款    2：未发货    3：已发货    4：已签收     5：退货申请    6：退货中    7：已退货    8：取消交易',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '下单时间',
  `paid_time` timestamp NULL DEFAULT NULL COMMENT '付款时间',
  `payment` int DEFAULT NULL COMMENT '付款金额',
  `user_id` int NOT NULL COMMENT '用户id',
  `good_id` int NOT NULL COMMENT '商品id',
  `number` int DEFAULT NULL COMMENT '秒杀数量',
  `flash_price` int DEFAULT NULL COMMENT '秒杀单价',
  `flash_cost` int DEFAULT NULL COMMENT '秒杀成本',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_flash_order`
--

LOCK TABLES `t_flash_order` WRITE;
/*!40000 ALTER TABLE `t_flash_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_flash_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good`
--

DROP TABLE IF EXISTS `t_good`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '产品名称',
  `stock` int DEFAULT NULL COMMENT '库存',
  `is_flash_sale` int DEFAULT NULL COMMENT '是否参加秒杀',
  `category_id` int DEFAULT NULL COMMENT '类别ID   例如：漾美丽保湿喷雾属于美妆类',
  `type` tinyint DEFAULT '1' COMMENT '0:虚拟(卡券） 1:实体',
  `selling_price` int DEFAULT NULL COMMENT '售价  int按分计算',
  `cost_price` int DEFAULT NULL COMMENT '进价  int按分计算',
  `num_scales` int DEFAULT NULL COMMENT '未知属性',
  `image_url` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '主图片url',
  `priority` int DEFAULT NULL COMMENT '优先级  越小越好',
  `add_coin` int DEFAULT NULL COMMENT '购买后给予多少积分',
  `model_id` int DEFAULT NULL COMMENT '模型id  如海底捞卡券属于火锅模型',
  `expired_time` timestamp NULL DEFAULT NULL COMMENT '过期时间',
  `parent_good_id` int DEFAULT NULL COMMENT '如果是套餐产品，这个是父商品id',
  `title` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '主标题        如糖醋鱼的标题是美食',
  `subtitle` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '副标题',
  `stock_cordon` int DEFAULT NULL COMMENT '库存警戒线',
  `status` tinyint DEFAULT '1' COMMENT '0: 下架   1: 上架   2：临期',
  `details` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '商品详情描述',
  `supplier_id` int DEFAULT NULL COMMENT '供应商id',
  `share_ratio` int DEFAULT NULL COMMENT '分成比例',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '添加时间',
  `last_update_time` timestamp NULL DEFAULT NULL COMMENT '最后修改时间',
  `saleable` tinyint(1) DEFAULT '1' COMMENT '0：下架\\\\r\\\\n     1：上架',
  `click_count` int DEFAULT NULL COMMENT '点击量',
  `transmit_count` int DEFAULT NULL COMMENT '转发量',
  `coinable` tinyint DEFAULT '0' COMMENT '0:可以使用积分\\\\r\\\\n  1:不可使用积分',
  `store_id` int DEFAULT NULL COMMENT '商家id',
  `price_line` int DEFAULT NULL COMMENT '商品划价线',
  `introducer_id` int DEFAULT NULL COMMENT '介绍人id',
  `sell_high` int DEFAULT NULL COMMENT '最高售价',
  `sell_low` int DEFAULT NULL COMMENT '最低售价',
  `cost_high` int DEFAULT NULL COMMENT '最高成本',
  `cost_low` int DEFAULT NULL COMMENT '最低成本',
  `display` tinyint DEFAULT '1' COMMENT '显示位置          1:顶部       0:底部',
  `coinable_number` int DEFAULT NULL COMMENT '积分可用数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good`
--

LOCK TABLES `t_good` WRITE;
/*!40000 ALTER TABLE `t_good` DISABLE KEYS */;
INSERT INTO `t_good` VALUES (4,'劳力士手表新款',100,1,1,1,50000,20000,200,'https://articleimg.xbiao.com/2023/0110/202301101673345375104.jpg',2,100,NULL,'2023-03-15 23:48:12',NULL,'表','新款手表',10,0,'吴亦凡同款手表',1,80,'2023-03-15 23:48:12','2023-03-15 23:48:12',1,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'海底捞卡券',200,1,2,0,20000,15000,100,'https://p3.itc.cn/q_70/images03/20210123/24a6faf9512241d38c46850ecd4585e6.png',1,100,3,'2023-04-15 23:48:12',NULL,'海底捞','石家庄海底捞消费券',5,1,'优惠券',2,90,'2023-03-14 23:48:12','2023-03-15 23:48:12',NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'糖醋里脊',400,0,2,1,2000,1000,500,'https://img1.baidu.com/it/u=1134263993,3633538136&fm=253&fmt=auto&app=138&f=JPEG?w=750&h=500',0,20,NULL,'2023-04-15 23:48:12',NULL,'美食','北京烤鸭',20,2,'好吃的烤鸭',4,70,'2023-03-14 23:48:12','2023-03-15 23:48:12',NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'漾美丽保湿喷雾',50,0,5,1,8000,2000,NULL,NULL,NULL,5,NULL,'2023-04-15 23:59:59',NULL,'美妆',NULL,NULL,NULL,NULL,NULL,66,'2023-03-14 23:48:12',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(37,'美团理发卡',0,0,0,0,0,0,0,'2003',0,0,0,'2023-03-22 00:57:14',0,'string','string',0,0,'string',0,0,'2023-03-22 00:57:14','2023-03-22 00:57:14',0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(38,'美团理发卡',0,0,0,0,0,0,0,'2003',0,0,0,'2023-03-22 00:57:14',0,'string','string',0,0,'string',0,0,'2023-03-22 00:57:14','2023-03-22 00:57:14',0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(39,'牛仔裤',0,0,0,1,0,0,0,'string',0,0,0,'2023-03-22 02:09:36',0,'string','string',0,0,'string',0,0,'2023-03-22 02:09:36','2023-03-22 02:09:36',0,0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL),(40,'SK神仙水',0,0,0,1,0,0,0,'string',0,0,0,'2023-03-22 03:13:48',0,'string','string',0,0,'string',0,0,'2023-03-22 03:13:48','2023-03-22 03:13:48',0,0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL),(54,'保温杯',0,0,0,1,0,0,0,'string',0,0,0,'2023-03-22 20:51:42',0,'string','string',0,0,'string',222,0,'2023-03-22 20:51:42','2023-03-22 20:51:42',0,0,0,0,0,0,111,NULL,NULL,NULL,NULL,NULL,NULL),(55,'保温杯',0,0,0,1,0,0,0,'string',0,0,0,'2023-03-22 20:51:42',0,'string','string',0,0,'string',222,0,'2023-03-22 20:51:42','2023-03-22 20:51:42',0,0,0,0,0,0,111,NULL,NULL,NULL,NULL,NULL,NULL),(56,'保温杯',0,0,0,1,0,0,0,'string',0,0,0,'2023-03-22 20:51:42',0,'string','string',0,0,'string',222,0,'2023-03-22 20:51:42','2023-03-22 20:51:42',0,0,0,0,0,0,111,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_good` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_category`
--

DROP TABLE IF EXISTS `t_good_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '类别名称  如烤鸭属于美食',
  `parent_category_id` int DEFAULT NULL COMMENT '父级类别名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_category`
--

LOCK TABLES `t_good_category` WRITE;
/*!40000 ALTER TABLE `t_good_category` DISABLE KEYS */;
INSERT INTO `t_good_category` VALUES (1,'百货',NULL),(2,'美食',NULL),(3,'美妆',NULL);
/*!40000 ALTER TABLE `t_good_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_image`
--

DROP TABLE IF EXISTS `t_good_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '商品图片url',
  `good_id` int DEFAULT NULL COMMENT '商品id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='一个商品存在多张图片';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_image`
--

LOCK TABLES `t_good_image` WRITE;
/*!40000 ALTER TABLE `t_good_image` DISABLE KEYS */;
INSERT INTO `t_good_image` VALUES (35,'1001',30),(36,'1002',30),(37,'2001',36),(38,'2002',36),(39,'2003',37),(40,'2004',37),(41,'2003',38),(42,'2004',38),(45,'string',39),(47,'哈哈',40),(56,'string',53),(57,'string',54),(58,'string',55),(59,'string',56),(60,'string',59),(61,'string',60),(62,'string',61),(63,'string',62),(64,'string',63);
/*!40000 ALTER TABLE `t_good_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_introducer`
--

DROP TABLE IF EXISTS `t_good_introducer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_introducer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '介绍人名称',
  `phone` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '介绍人电话',
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '介绍人住址',
  `id_card` varchar(25) DEFAULT NULL COMMENT '介绍人身份证',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_introducer`
--

LOCK TABLES `t_good_introducer` WRITE;
/*!40000 ALTER TABLE `t_good_introducer` DISABLE KEYS */;
INSERT INTO `t_good_introducer` VALUES (1,'string','string','string','string'),(111,'string','string','string','string');
/*!40000 ALTER TABLE `t_good_introducer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_model`
--

DROP TABLE IF EXISTS `t_good_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_model` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_model`
--

LOCK TABLES `t_good_model` WRITE;
/*!40000 ALTER TABLE `t_good_model` DISABLE KEYS */;
INSERT INTO `t_good_model` VALUES (1,'烧烤'),(2,'保湿'),(3,'火锅'),(4,'剪发');
/*!40000 ALTER TABLE `t_good_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_priority`
--

DROP TABLE IF EXISTS `t_good_priority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_priority` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_priority`
--

LOCK TABLES `t_good_priority` WRITE;
/*!40000 ALTER TABLE `t_good_priority` DISABLE KEYS */;
INSERT INTO `t_good_priority` VALUES (1,'爆款推荐'),(2,'9.9包邮'),(3,'店长推荐');
/*!40000 ALTER TABLE `t_good_priority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_spec`
--

DROP TABLE IF EXISTS `t_good_spec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_spec` (
  `good_id` int DEFAULT NULL COMMENT '商品id',
  `price` int DEFAULT NULL COMMENT '售价',
  `cost` int DEFAULT NULL COMMENT '成本',
  `value` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '规格的值    例如：糖醋里脊的甜口、酸口',
  `id` int NOT NULL AUTO_INCREMENT,
  `stock` int DEFAULT NULL COMMENT '库存',
  `price_line` int DEFAULT NULL COMMENT '划价线',
  `image` varchar(256) DEFAULT NULL COMMENT '图片url',
  PRIMARY KEY (`id`),
  UNIQUE KEY `t_specs_un` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='一个商品存在多个规格    关联商品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_spec`
--

LOCK TABLES `t_good_spec` WRITE;
/*!40000 ALTER TABLE `t_good_spec` DISABLE KEYS */;
INSERT INTO `t_good_spec` VALUES (7,2000,1000,'甜口的糖醋里脊',1,NULL,NULL,NULL),(7,2500,1300,'酸口的糖醋里脊',2,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_good_spec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_spec_image`
--

DROP TABLE IF EXISTS `t_good_spec_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_spec_image` (
  `id` int NOT NULL,
  `spec_id` int DEFAULT NULL COMMENT '规格id',
  `image` varchar(256) DEFAULT NULL COMMENT '图片url',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_spec_image`
--

LOCK TABLES `t_good_spec_image` WRITE;
/*!40000 ALTER TABLE `t_good_spec_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_good_spec_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_store`
--

DROP TABLE IF EXISTS `t_good_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_store` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL COMMENT '店铺名称',
  `phone` varchar(45) DEFAULT NULL COMMENT '电话',
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(45) DEFAULT NULL COMMENT '城市',
  `area` varchar(45) DEFAULT NULL COMMENT '区域',
  `street` varchar(45) DEFAULT NULL COMMENT '街道',
  `address` varchar(45) DEFAULT NULL COMMENT '详细地址',
  `status` tinyint DEFAULT NULL COMMENT '店铺状态   0:已关停  1:待审核   2:已审核',
  `owner` varchar(45) DEFAULT NULL COMMENT '店铺拥有人',
  `recommender_id` int DEFAULT NULL COMMENT '推荐人id',
  `register_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_store`
--

LOCK TABLES `t_good_store` WRITE;
/*!40000 ALTER TABLE `t_good_store` DISABLE KEYS */;
INSERT INTO `t_good_store` VALUES (25,'海底捞石家庄店','18855556666',NULL,'石家庄',NULL,NULL,NULL,NULL,NULL,NULL,'2023-03-30 03:18:10');
/*!40000 ALTER TABLE `t_good_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_supplier`
--

DROP TABLE IF EXISTS `t_good_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_supplier` (
  `id` int NOT NULL,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '供应商名称',
  `phone` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '供应商电话',
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '供应商地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_supplier`
--

LOCK TABLES `t_good_supplier` WRITE;
/*!40000 ALTER TABLE `t_good_supplier` DISABLE KEYS */;
INSERT INTO `t_good_supplier` VALUES (1,'劳力士北京店','18888889999','东单大街'),(2,'石家庄海底捞店','19934567890','西单大街'),(3,'石家庄漾美丽科技有限公司','18823456789','眼科医院宿舍'),(4,'string','string','string'),(222,'222提供的','string','string');
/*!40000 ALTER TABLE `t_good_supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_text`
--

DROP TABLE IF EXISTS `t_good_text`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_text` (
  `id` int NOT NULL AUTO_INCREMENT,
  `good_id` int DEFAULT NULL COMMENT '商品id',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '图文详情   图片和文字放在一起',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_text`
--

LOCK TABLES `t_good_text` WRITE;
/*!40000 ALTER TABLE `t_good_text` DISABLE KEYS */;
INSERT INTO `t_good_text` VALUES (2,40,'狗屁神仙水','2023-03-22 11:15:01'),(3,41,'string','2023-03-22 18:52:32'),(4,42,'string','2023-03-22 19:25:02'),(5,43,'string','2023-03-22 19:53:51'),(6,44,'string','2023-03-22 19:53:51'),(7,45,'string','2023-03-22 19:53:51'),(8,46,'string','2023-03-22 19:53:51'),(9,52,'string','2023-03-22 20:51:42'),(10,53,'string','2023-03-22 20:51:42'),(11,54,'string','2023-03-22 20:51:42'),(12,55,'string','2023-03-22 20:51:42'),(13,56,'string','2023-03-22 20:51:42'),(14,59,'string','2023-03-23 18:50:28'),(15,60,'string','2023-03-23 18:50:28'),(16,61,'string','2023-03-23 18:50:28'),(17,62,'string','2023-03-23 18:50:28'),(18,63,'string','2023-03-23 18:50:28');
/*!40000 ALTER TABLE `t_good_text` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_good_type`
--

DROP TABLE IF EXISTS `t_good_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_good_type` (
  `id` int NOT NULL,
  `type` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_good_type`
--

LOCK TABLES `t_good_type` WRITE;
/*!40000 ALTER TABLE `t_good_type` DISABLE KEYS */;
INSERT INTO `t_good_type` VALUES (0,'卡券'),(1,'实体');
/*!40000 ALTER TABLE `t_good_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_level`
--

DROP TABLE IF EXISTS `t_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_level`
--

LOCK TABLES `t_level` WRITE;
/*!40000 ALTER TABLE `t_level` DISABLE KEYS */;
INSERT INTO `t_level` VALUES (0,'普通会员'),(1,'活跃会员'),(2,'团长'),(3,'王者');
/*!40000 ALTER TABLE `t_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_lock_balance`
--

DROP TABLE IF EXISTS `t_lock_balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_lock_balance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '外键',
  `change` int NOT NULL DEFAULT '0' COMMENT '变动',
  `lock_balance` int NOT NULL COMMENT '锁定金额',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型',
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '描述',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_lock_balance`
--

LOCK TABLES `t_lock_balance` WRITE;
/*!40000 ALTER TABLE `t_lock_balance` DISABLE KEYS */;
INSERT INTO `t_lock_balance` VALUES (1,9,0,500,'未知字段','小明的账户锁定额','2023-02-13 22:15:02'),(2,10,0,1000,'未知字段','小红的账户锁定额','2023-02-13 22:15:02');
/*!40000 ALTER TABLE `t_lock_balance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_mall_order`
--

DROP TABLE IF EXISTS `t_mall_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_mall_order` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `good_id` int DEFAULT NULL COMMENT '商品id',
  `sku_id` int DEFAULT NULL COMMENT '规格id   例如：如果一件衣服有红色、白色和蓝色，SKU代码就不同',
  `user_id` int DEFAULT NULL COMMENT '用户id',
  `sale_price` int DEFAULT NULL COMMENT '售价',
  `cost_price` int DEFAULT NULL COMMENT '成本',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `paid_time` timestamp NULL DEFAULT NULL COMMENT '支付时间',
  `status` tinyint DEFAULT NULL COMMENT '状态   0：未付款    1：已付款    2：未发货    3：已发货    4：已签收     5：退货申请    6：退货中    7：已退货    8：取消交易',
  `number` int DEFAULT NULL COMMENT '数量',
  `address` varchar(128) DEFAULT NULL COMMENT '收货地址',
  `phone` varchar(25) DEFAULT NULL COMMENT '联系电话',
  `store_id` int DEFAULT NULL COMMENT '店铺id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_mall_order`
--

LOCK TABLES `t_mall_order` WRITE;
/*!40000 ALTER TABLE `t_mall_order` DISABLE KEYS */;
INSERT INTO `t_mall_order` VALUES (16,4,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',0,1,NULL,NULL,NULL),(21,5,218,9,20000,15000,'2023-03-15 21:54:46','2023-03-15 21:54:46',1,2,NULL,NULL,NULL),(22,6,217,10,10000,5000,'2023-03-15 21:54:46','2023-03-15 21:54:46',2,2,NULL,NULL,NULL),(23,7,318,10,2000,1000,'2023-03-15 21:54:46','2023-03-15 21:54:46',3,3,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_mall_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_model`
--

DROP TABLE IF EXISTS `t_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_model` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_model`
--

LOCK TABLES `t_model` WRITE;
/*!40000 ALTER TABLE `t_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_order`
--

DROP TABLE IF EXISTS `t_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_order` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `good_id` int DEFAULT NULL COMMENT '商品id',
  `sku_id` int DEFAULT NULL COMMENT '规格id   例如：如果一件衣服有红色、白色和蓝色，SKU代码就不同',
  `paider_id` int DEFAULT NULL COMMENT '付款人id',
  `sale_price` int DEFAULT NULL COMMENT '售价',
  `cost_price` int DEFAULT NULL COMMENT '成本',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '创建时间    与支付时间有本质区别',
  `paid_time` timestamp NULL DEFAULT NULL COMMENT '支付时间',
  `status_id` tinyint NOT NULL COMMENT '状态id        对应未发货、已发货、已完成',
  `number` int DEFAULT NULL COMMENT '商品数量',
  `consignee_address` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '收货人地址',
  `consignee_phone` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '收货人联系电话',
  `store_id` int DEFAULT NULL COMMENT '商家id',
  `paid_amount` int DEFAULT NULL COMMENT '实际支付的现金',
  `delivery_fee` int DEFAULT NULL COMMENT '运费金额',
  `spec_id` int DEFAULT NULL COMMENT '规格编号',
  `paid_coin` int DEFAULT NULL COMMENT '实际支付的积分',
  `delivery_track_code` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '物流单号（追踪吗）  比如顺丰的单号',
  `paid_channel_id` int DEFAULT NULL COMMENT '支付渠道    比如余额支付  微信支付  银行卡支付',
  `consignee_name` varchar(25) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '收货人名称',
  `delivery_time` timestamp NULL DEFAULT NULL COMMENT '发货时间',
  `supplier_id` int DEFAULT NULL COMMENT '供应商id',
  `good_name` varchar(45) DEFAULT NULL COMMENT '商品名称',
  `paid_track_code` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '支付订单号（追踪码）    比如微信支付提供的支付编码',
  `paider_name` varchar(100) DEFAULT NULL COMMENT '付款人姓名',
  `paider_phone` varchar(100) DEFAULT NULL COMMENT '付款人电话',
  `paider_address` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '付款人地址',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3 COMMENT='发货订单表（不包含秒杀订单)    1.创建时间与支付时间有本质区别';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_order`
--

LOCK TABLES `t_order` WRITE;
/*!40000 ALTER TABLE `t_order` DISABLE KEYS */;
INSERT INTO `t_order` VALUES (16,4,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',0,1,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,50000,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',1,'漾美丽保湿喷雾','wx8086645456',NULL,NULL,NULL),(21,5,218,9,20000,15000,'2023-03-15 21:54:46','2023-03-15 21:54:46',1,2,'','',25,18000,NULL,NULL,NULL,'',1,'小明',NULL,3,NULL,'wx8086455645',NULL,NULL,NULL),(22,6,217,10,10000,5000,'2023-03-15 21:54:46','2023-03-15 21:54:46',2,2,'北京朝阳区三路屯梦幻酒吧2楼包间','16699992222',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小红','2023-03-15 23:48:12',2,NULL,NULL,NULL,NULL,NULL),(23,7,318,10,2000,1000,'2023-03-15 21:54:46','2023-03-15 21:54:46',3,3,'北京朝阳区三路屯梦幻酒吧2楼包间','16699992222',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小红','2023-03-15 23:48:12',4,NULL,NULL,NULL,NULL,NULL),(24,6,217,10,10000,5000,'2023-03-15 21:54:46','2023-03-15 21:54:46',2,2,'北京朝阳区三路屯梦幻酒吧2楼包间','16699992222',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小红','2023-03-15 23:48:12',3,NULL,NULL,NULL,NULL,NULL),(25,4,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',0,1,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',2,'海底捞卡券','wx8086455645',NULL,NULL,NULL),(26,5,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',0,1,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',1,'漾美丽保湿喷雾','wx8086645456',NULL,NULL,NULL),(27,5,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',0,1,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',1,'漾美丽保湿喷雾','wx8086645456',NULL,NULL,NULL),(28,4,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-16 21:54:46',1,1,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,NULL,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',1,'漾美丽保湿面膜','wx8086645456',NULL,NULL,NULL),(29,4,212,9,50000,20000,'2023-03-16 21:54:46','2023-03-28 21:54:46',1,2,'北京朝阳区三路屯梦幻酒吧2楼包间','18855556666',NULL,16888,NULL,NULL,NULL,'SF10086',1,'小明','2023-03-15 23:48:12',1,'漾美丽防晒霜','wx8086645456',NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_order_return`
--

DROP TABLE IF EXISTS `t_order_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_order_return` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '退货编号',
  `returner_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '退款人姓名',
  `returner_phone` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '退款人电话',
  `returner_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '退款人地址',
  `delivery_fee` int DEFAULT NULL COMMENT '退货运费',
  `return_amount` int DEFAULT NULL COMMENT '退款金额',
  `return_submit_time` timestamp NULL DEFAULT NULL COMMENT '退货申请时间',
  `return_reason` varchar(128) DEFAULT NULL COMMENT '退货原因',
  `order_id` int NOT NULL COMMENT '订单编号',
  `supplier_id` int DEFAULT NULL COMMENT '供应商id',
  `good_id` int NOT NULL COMMENT '商品id',
  `return_num` int DEFAULT NULL COMMENT '退货换数量',
  `store_id` int DEFAULT NULL COMMENT '商家id',
  `return_delivery_track_code` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '物流单号   追踪码',
  `status_id` tinyint DEFAULT NULL COMMENT '状态id     对应退款协商中、未处理、已退货',
  `consignee_name` varchar(100) DEFAULT NULL COMMENT '收货人姓名',
  `consignee_phone` varchar(100) DEFAULT NULL COMMENT '收货人电话',
  `consignee_address` varchar(100) DEFAULT NULL COMMENT '收货人地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='退货订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_order_return`
--

LOCK TABLES `t_order_return` WRITE;
/*!40000 ALTER TABLE `t_order_return` DISABLE KEYS */;
INSERT INTO `t_order_return` VALUES (1,'小明','18132221182',NULL,NULL,NULL,NULL,'假冒伪劣',16,NULL,4,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_order_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_order_return_state`
--

DROP TABLE IF EXISTS `t_order_return_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_order_return_state` (
  `id` int NOT NULL AUTO_INCREMENT,
  `state` varchar(25) DEFAULT NULL COMMENT '退换货状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_order_return_state`
--

LOCK TABLES `t_order_return_state` WRITE;
/*!40000 ALTER TABLE `t_order_return_state` DISABLE KEYS */;
INSERT INTO `t_order_return_state` VALUES (1,'已退货'),(2,'未处理'),(3,'协商中');
/*!40000 ALTER TABLE `t_order_return_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_order_return_type`
--

DROP TABLE IF EXISTS `t_order_return_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_order_return_type` (
  `id` int NOT NULL,
  `type` varchar(45) DEFAULT NULL COMMENT '类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单退货类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_order_return_type`
--

LOCK TABLES `t_order_return_type` WRITE;
/*!40000 ALTER TABLE `t_order_return_type` DISABLE KEYS */;
INSERT INTO `t_order_return_type` VALUES (1,'全部退货退款'),(2,'全部换货'),(3,'部分退货退款'),(4,'部分换货');
/*!40000 ALTER TABLE `t_order_return_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_order_state`
--

DROP TABLE IF EXISTS `t_order_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_order_state` (
  `id` int NOT NULL AUTO_INCREMENT,
  `state` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '订单状态',
  `belong` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '所属订单类别   比如发货  退货',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单状态表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_order_state`
--

LOCK TABLES `t_order_state` WRITE;
/*!40000 ALTER TABLE `t_order_state` DISABLE KEYS */;
INSERT INTO `t_order_state` VALUES (1,'未发货','send'),(2,'已发货','send'),(3,'退货协商中','return'),(4,'未处理','return'),(5,'已退货','return'),(6,'已完成','finish');
/*!40000 ALTER TABLE `t_order_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_package`
--

DROP TABLE IF EXISTS `t_package`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_package` (
  `id` int NOT NULL AUTO_INCREMENT,
  `good_id` int NOT NULL COMMENT '产品id',
  `amount` int DEFAULT NULL COMMENT '份数;the number of good in one amount一个包包含的产品的数量',
  `flash_sale_price` int DEFAULT NULL COMMENT '秒杀价格;in cent,秒杀价格',
  `num` int DEFAULT NULL COMMENT '包个数;一共有多少个包',
  `stock` int DEFAULT NULL COMMENT '剩余包数量',
  `seller_id` int DEFAULT NULL COMMENT '发布商品的卖家，如果id为空或者0，则为官方卖家',
  `spec_id` int DEFAULT NULL COMMENT '规格id',
  `share_fee` int DEFAULT NULL COMMENT '让利金额',
  `status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_package`
--

LOCK TABLES `t_package` WRITE;
/*!40000 ALTER TABLE `t_package` DISABLE KEYS */;
INSERT INTO `t_package` VALUES (1,7,10,30,125,125,0,1,5,NULL);
/*!40000 ALTER TABLE `t_package` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_package_time`
--

DROP TABLE IF EXISTS `t_package_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_package_time` (
  `id` int NOT NULL AUTO_INCREMENT,
  `start_time` int DEFAULT NULL COMMENT '开始时间;9*3600表示9:00',
  `end_time` int DEFAULT NULL COMMENT '结束时间;以秒为单位',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_package_time`
--

LOCK TABLES `t_package_time` WRITE;
/*!40000 ALTER TABLE `t_package_time` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_package_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_package_time_pair`
--

DROP TABLE IF EXISTS `t_package_time_pair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_package_time_pair` (
  `id` int NOT NULL AUTO_INCREMENT,
  `package_id` int DEFAULT NULL,
  `package_time_id` int DEFAULT NULL,
  `status` int DEFAULT NULL COMMENT '状态; 0: 未激活, 1: 激活',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_package_time_pair`
--

LOCK TABLES `t_package_time_pair` WRITE;
/*!40000 ALTER TABLE `t_package_time_pair` DISABLE KEYS */;
INSERT INTO `t_package_time_pair` VALUES (1,1,1,1);
/*!40000 ALTER TABLE `t_package_time_pair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_pay_channel`
--

DROP TABLE IF EXISTS `t_pay_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_pay_channel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL COMMENT '支付方式',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_pay_channel`
--

LOCK TABLES `t_pay_channel` WRITE;
/*!40000 ALTER TABLE `t_pay_channel` DISABLE KEYS */;
INSERT INTO `t_pay_channel` VALUES (1,'微信支付'),(2,'银行卡支付'),(3,'余额支付');
/*!40000 ALTER TABLE `t_pay_channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_product`
--

DROP TABLE IF EXISTS `t_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL COMMENT 'product name产品名称',
  `stock` int DEFAULT NULL COMMENT '库存',
  `is_flash_sale` int DEFAULT NULL COMMENT '是否已经参加了秒杀',
  `category_id` int DEFAULT NULL COMMENT '类别ID',
  `type` varchar(45) DEFAULT NULL COMMENT 'is real or virtual， 虚拟类型还是实体类型，只能有两个值real和virtual',
  `selling_price` int DEFAULT NULL COMMENT 'in cent - 1/100 yuan,售价',
  `cost_price` int DEFAULT NULL COMMENT '进价',
  `num_scales` int DEFAULT NULL,
  `image_url` varchar(256) DEFAULT NULL COMMENT '图片地址，如果用逗号隔开，表明有多个图片',
  `priority` int DEFAULT NULL COMMENT 'less is better，优先级，越小越好',
  `sliver_coin` int DEFAULT NULL COMMENT '购买后给予多少银币',
  `model_id` int DEFAULT NULL COMMENT '型号id',
  `expired_time` timestamp NULL DEFAULT NULL COMMENT '过期时间',
  `parent_product_id` int DEFAULT NULL COMMENT '如果是套餐产品，这个是父产品id',
  `title` varchar(45) DEFAULT NULL COMMENT '产品标题',
  `subtitle` varchar(45) DEFAULT NULL COMMENT '副产品标题',
  `stock_cordon` int DEFAULT NULL COMMENT '库存警戒线',
  `status` varchar(45) DEFAULT NULL COMMENT '状态',
  `details` varchar(512) DEFAULT NULL COMMENT '商品详情图片列表，以逗号隔开',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_product`
--

LOCK TABLES `t_product` WRITE;
/*!40000 ALTER TABLE `t_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_sale_product`
--

DROP TABLE IF EXISTS `t_sale_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_sale_product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `balance` int DEFAULT NULL COMMENT 'in cent',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_sale_product`
--

LOCK TABLES `t_sale_product` WRITE;
/*!40000 ALTER TABLE `t_sale_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_sale_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_store`
--

DROP TABLE IF EXISTS `t_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_store` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) DEFAULT NULL COMMENT '店铺名称',
  `phone` varchar(45) DEFAULT NULL COMMENT '电话',
  `province` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '省份',
  `city` varchar(45) DEFAULT NULL COMMENT '城市',
  `area` varchar(45) DEFAULT NULL COMMENT '区域',
  `street` varchar(45) DEFAULT NULL COMMENT '街道',
  `address` varchar(45) DEFAULT NULL COMMENT '详细地址',
  `status` varchar(45) DEFAULT NULL,
  `owner` varchar(45) DEFAULT NULL COMMENT '店铺拥有人',
  `recommender_id` int DEFAULT NULL COMMENT '推荐人id',
  `register_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `parent_store_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_store`
--

LOCK TABLES `t_store` WRITE;
/*!40000 ALTER TABLE `t_store` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_store_membership`
--

DROP TABLE IF EXISTS `t_store_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_store_membership` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  `expired_time` timestamp NULL DEFAULT NULL COMMENT '过期时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_store_membership`
--

LOCK TABLES `t_store_membership` WRITE;
/*!40000 ALTER TABLE `t_store_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_store_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_user` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '用户名',
  `email` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '邮箱',
  `open_id` varchar(45) DEFAULT NULL COMMENT 'openID from wechat channel',
  `union_id` varchar(45) DEFAULT NULL COMMENT 'unionID from tecent',
  `password` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '密码（哈希值）',
  `nickname` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '昵称',
  `phone` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '联系方式',
  `id_card` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '身份证',
  `level_id` int DEFAULT '1' COMMENT '等级',
  `status` tinyint DEFAULT NULL COMMENT '0: 已实名   1: 未实名',
  `register_time` timestamp NULL DEFAULT NULL COMMENT '注册时间',
  `avatar` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '头像url',
  `invited_user_id` int DEFAULT NULL COMMENT '推荐人id',
  `balance` int DEFAULT NULL COMMENT '余额',
  `coin` float DEFAULT NULL COMMENT '积分',
  `gender` tinyint DEFAULT NULL COMMENT '0:  男  1:  女',
  `last_active_time` timestamp NULL DEFAULT NULL COMMENT '最近登录时间',
  `name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '用户名',
  `lock` tinyint DEFAULT '1' COMMENT '0:封禁    1:未封禁',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COMMENT='user';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (9,'小明','ls973383360@163.com','olmhl5FhSg-ICcVjm7hZZCIEylz4','olmhl5FhSg-ICcVjm7hZZCIEylz4','123456','钢蛋','18132221182','130682199701262713',2,1,'2023-03-12 21:58:20','https://img0.baidu.com/it/u=2796569578,3631038492&fm=253&fmt=auto&app=138&f=JPEG?w=270&h=319',NULL,1000,1000,0,'2023-03-16 07:58:20','小明',1),(10,'小红','xiaohong@QQ.com',NULL,NULL,'234567','漂亮姑娘','18812345678','130682199806248916',3,1,'2023-03-12 21:58:20','https://pic.rmb.bdstatic.com/6696bd1063b857321b3d4d0a387e0b98.jpeg',9,500,200,1,'2023-03-10 07:58:20','小红',1),(11,'钢蛋',NULL,NULL,NULL,'123456','肯塔基州的钢蛋','18812345678','130682199806248916',1,1,NULL,'https://inews.gtimg.com/newsapp_bt/0/14129750268/641',NULL,NULL,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user_account`
--

DROP TABLE IF EXISTS `t_user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_user_account` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '账户id',
  `user_id` int NOT NULL COMMENT '用户id',
  `balance` int NOT NULL DEFAULT '0' COMMENT '余额',
  `lock_balance` int NOT NULL DEFAULT '0' COMMENT '锁定额',
  `coin` int NOT NULL DEFAULT '0' COMMENT '积分',
  `description` varchar(100) DEFAULT NULL COMMENT '详细描述',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录生成时间',
  `bank_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '开户行',
  `id_card` varchar(45) DEFAULT NULL COMMENT '银行账号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user_account`
--

LOCK TABLES `t_user_account` WRITE;
/*!40000 ALTER TABLE `t_user_account` DISABLE KEYS */;
INSERT INTO `t_user_account` VALUES (0,9,100000,500,0,'小明的建行账户','2023-03-13 22:15:02','石家庄高新区天山支行','622538652376856283'),(1,10,200000,1000,0,'小红的工行账户','2023-03-13 23:12:26','北京市朝阳区国贸支行','622538652376856288');
/*!40000 ALTER TABLE `t_user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user_bank`
--

DROP TABLE IF EXISTS `t_user_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_user_bank` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '开户行',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '户主姓名',
  `id_card` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '银行卡号',
  `user_id` int DEFAULT NULL COMMENT '用户id',
  `phone` varchar(25) DEFAULT NULL COMMENT '户主电话',
  `bank_address` varchar(100) DEFAULT NULL COMMENT '开户行地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user_bank`
--

LOCK TABLES `t_user_bank` WRITE;
/*!40000 ALTER TABLE `t_user_bank` DISABLE KEYS */;
INSERT INTO `t_user_bank` VALUES (1,'石家庄高新区天山支行','小明','622538652376856283',9,NULL,NULL);
/*!40000 ALTER TABLE `t_user_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user_favs`
--

DROP TABLE IF EXISTS `t_user_favs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_user_favs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `good_id` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user_favs`
--

LOCK TABLES `t_user_favs` WRITE;
/*!40000 ALTER TABLE `t_user_favs` DISABLE KEYS */;
INSERT INTO `t_user_favs` VALUES (14,'9','4','2023-03-15 08:46:42'),(16,'10','6','2023-03-15 08:46:42');
/*!40000 ALTER TABLE `t_user_favs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user_level`
--

DROP TABLE IF EXISTS `t_user_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_user_level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user_level`
--

LOCK TABLES `t_user_level` WRITE;
/*!40000 ALTER TABLE `t_user_level` DISABLE KEYS */;
INSERT INTO `t_user_level` VALUES (0,'普通会员'),(1,'活跃会员'),(2,'团长'),(3,'王者');
/*!40000 ALTER TABLE `t_user_level` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-03  9:24:49
