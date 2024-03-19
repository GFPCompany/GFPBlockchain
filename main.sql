/*
 Navicat Premium Data Transfer

 Source Server         : gfp_db
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 19/03/2024 23:07:19
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for blocks
-- ----------------------------
DROP TABLE IF EXISTS "blocks";
CREATE TABLE "blocks" (
  "id" integer,
  "hash" integer,
  "timestamp" integer,
  "nonce" integer,
  "transactions" TEXT,
  "previous_hash" VARCHAR
);

-- ----------------------------
-- Records of blocks
-- ----------------------------
INSERT INTO "blocks" VALUES (0, 0, 252452, 24, '{"transaction":0}', NULL);

-- ----------------------------
-- Table structure for peers
-- ----------------------------
DROP TABLE IF EXISTS "peers";
CREATE TABLE "peers" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "address" TEXT,
  "port" integer(255),
  "version" integer(255),
  "height" integer(255),
  "token" TEXT
);

-- ----------------------------
-- Records of peers
-- ----------------------------
INSERT INTO "peers" VALUES (1, '127.0.0.1', 57371, '0.0.1', 0, '89d3dcfb78b037370d17f9f9ba308b3039f7a3a993317872348eee12e362248f1f832f5a117caf1ac10f09aae50470b4eda7e959c2e3212e0e0059d7fc3ccba6');

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
INSERT INTO "sqlite_sequence" VALUES ('peers', 1);

-- ----------------------------
-- Auto increment value for peers
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'peers';

PRAGMA foreign_keys = true;
