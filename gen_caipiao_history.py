from HTMLParser import HTMLParser
import requests
import re

#shuang se qiu
#r = requests.get("http://chart.cp.360.cn/kaijiang/ssq/?lotId=220051&chartType=undefined&spanType=0&span=2000&r=0.9696977403296737#roll_0")

# da le tou
r = requests.get("http://chart.cp.360.cn/kaijiang/slt?lotId=120029&chartType=undefined&spanType=0&span=2000&r=0.5524914922822491#roll_132")
str_test = r.content.strip()
 
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.datas = []
 
    def handle_data(self, data):
        #print "Encountered the beginning of a %s tag" % tag
        self.datas.append(data)

 
def filter_ssq(data_list):
    index = 0
    result = []
    ssq_id = re.compile(r'(20\d+)')
    ssq_date = re.compile(r'(20\d+\-\d+\-\d+)')
    ssq_ball = re.compile(r'(\d+)')
    while index < len(data_list):
        s_id = ssq_id.search(str(data_list[index]))
        data = []
        if s_id:
            data.append(s_id.groups()[0])        
            s_date = ssq_date.search(str(data_list[index+1]))
            if s_date:
                data.append(s_date.groups()[0])
                for i in range(2,9):
                    s_ball = ssq_ball.search(str(data_list[index+i]))
                    if s_ball:
                         data.append(s_ball.groups()[0])
        if len(data) == 9:
            index += 9
            result.append(data)
        else:
            index += 1 
    return result


if __name__ == "__main__":
    hp = MyHTMLParser()
    hp.feed(str_test)
    ssq_list = filter_ssq(hp.datas)
    for ssq in ssq_list:
        print " ".join(ssq)
    hp.close()
