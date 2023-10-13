# 此程式為一個對動態網頁的爬蟲

## 基本上只要安裝完 database 和 python 就可以使用了

### database

#### 原則上這一個步驟只要執行一次,除非有要把資料庫翻掉

1. `docker pull mysql/mysql-server:8.0`
2. `docker run --name=mysql8 -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=test -e MYSQL_USER=test -e MYSQL_PASSWORD=test -e MYSQL_DATABASE=localTest3 mysql/mysql-server:8.0 --default-authentication-plugin=mysql_native_password`
3. `docker exec -i mysql8 mysql  -utest -ptest localTest3 < backup.sql`

### python3

請務必先安裝安裝 python3.0.0 以上版本(pip 記得要一起裝) 2.直接使用 make local-run 就可以了(如果有報錯應該是 pip 有些東西沒裝到 有漏什麼就裝什麼)


### 結語
經年累月後,網站可能已經不在了,不過爬蟲的做法可以參考以下這篇文章的動態網頁部分  
- [爬蟲教學參考文章](https://ithelp.ithome.com.tw/articles/10282931)  
