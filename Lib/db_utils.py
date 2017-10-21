#encoding=utf-8
import  pymysql
import  sys
reload(sys)
sys.setdefaultencoding('utf-8')
class db_utils:
    def __init__(self):
        self.conn = pymysql.connect(host='114.55.6.228', port=3306, user='slave_user_copyA', passwd='slave_pwd_copyA', db='sxb',charset='utf8')
        self.cursor = self.conn.cursor()

    def fetchmany(self,sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception, e:
            print e
            print sql

    def fetchone(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except Exception, e:
            print e
            print sql

    def close_db(self):
        self.cur.close()
        self.conn.close()

    def get_car_by_series(self, series):
        if series != '':
            print '=============', series
            sql = "SELECT s.series,truncate(s.officialQuote/100,0)price,s.market,carLocation,CONCAT(LEFT(u.realName,1),'经理') realname,s.favorableDot from salescar s INNER JOIN `user` u on u.id=s.`user` WHERE s.series='" + series + "' ORDER BY s.officialQuote desc LIMIT 10 "
            cardate = self.fetchmany(sql)
            cartext = '【今日省心宝资源价格】\n'
            for car in cardate:
                market = car[2]
                if abs(int(market)) > 30000:
                    market = car[5]
                if market < 0:
                    market = '下' + str(abs(float(market)))
                else:
                    market = '上' + str(market)
                cartext = cartext + '   ' + car[0] + '   ' + str(car[1]) + '   ' + market + '   ' + car[3] + '   ' + \
                          car[4] + "\n"
            if cardate:
                cartext = cartext + '\n\n' + '更多行情信息，请点击 http://h5.sxbcar.com/d 下载APP联系卖方购买！'
            else:
                cartext = '暂无车源信息,看看其他的车源吧！'
            return cartext
        else:
            return ''



