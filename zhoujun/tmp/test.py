#coding:utf-8
import time

class Workday(object):

    def getDateByTime(self):
            self.myDate = []
            t = str(time.strftime('%Y-%m-'))
            for i in range(1, 32):
                timeStr = t + str(i)
                try:
                    #字符串转换为规定格式的时间
                    tmp = time.strptime(timeStr, '%Y-%m-%d')
                    #判断是否为周六、周日
                    if (tmp.tm_wday != 6) and (tmp.tm_wday != 5):
                        self.myDate.append(time.strftime('%Y-%m-%d', tmp))
                except:
                    print('日期越界')
            if len(self.myDate) == 0:
                self.myDate.append(time.strftime('%Y-%m-%d'))
            return self.myDate

if __name__ == '__main__':
    day = Workday()
    print day.getDateByTime() 
    