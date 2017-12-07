/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50712
Source Host           : localhost:3306
Source Database       : StockCrawler

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2017-12-07 11:29:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for DailyData
-- ----------------------------
DROP TABLE IF EXISTS `DailyData`;
CREATE TABLE `DailyData` (
  `StockId` varchar(10) NOT NULL,
  `TradeDate` date NOT NULL,
  `Volume` varchar(50) DEFAULT NULL,
  `Turnover` varchar(50) DEFAULT NULL,
  `Opening` varchar(15) DEFAULT NULL,
  `Highest` varchar(15) DEFAULT NULL,
  `Lowest` varchar(15) DEFAULT NULL,
  `Closing` varchar(15) DEFAULT NULL,
  `QuoteChange` varchar(15) DEFAULT NULL,
  `TransNum` varchar(50) DEFAULT NULL,
  `CreateDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`StockId`,`TradeDate`),
  KEY `INX01` (`StockId`),
  KEY `INX02` (`TradeDate`),
  KEY `INX03` (`QuoteChange`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
