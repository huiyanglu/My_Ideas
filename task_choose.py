"""
每周任务选择计划安排
---
5.30下班
6.00到宿舍
6.00-6.30 吃零食站墙看电视
6.30-12.00 5.5h
---
6项任务每天任选4-5项
任务总时间不超过5h
每项任务需要多长时间完成
每项任务每天可以做多长时间
每做一次完成的百分比
平衡各项任务之间的任务进度 一周下来 差距不超过20%

"""
import random

class Task():
    def __init__(self):
        self.todolist = ['《入门》项目 1h',
                    '《流畅》看书 1h',
                    'aiyo爬虫教程 2h',
                    '统计学习看书 1h',
                    'LeetCode刷题 1.5h',
                    '数据结构看书 1h',
                    'Excel教程 1h']
        self.todolist2 = {'《入门》项目1h': '1',
                          '《流畅》看书1h': '1',
                          'aiyo爬虫教程2h': '2',
                          '统计学习看书1h': '1',
                          'LeetCode刷题1.5h': '1.5',
                          '数据结构看书1h': '1'}
        self.finished_task = {'《入门》项目1h': '10',
                              '《流畅》看书1h': '10',
                              'aiyo爬虫教程2h': '10',
                              '统计学习看书1h': '20',
                              'LeetCode刷题1.5h': '20',
                              '数据结构看书1h': '10'}
        self.finished_percent = {'《入门》项目1h': 0,
                                '《流畅》看书1h': 0,
                                'aiyo爬虫教程2h': 0,
                                '统计学习看书1h': 0,
                                'LeetCode刷题1.5h': 0,
                                '数据结构看书1h': 0}

    def percent(self,choose_each):
        """每个任务所占的比重"""
        perc = float(self.todolist2[choose_each])/float(self.finished_task[choose_each])
        return perc

    def choose_one(self):
        """每天的计划（不超过5.5h）"""
        rst = []
        hour = 0
        while hour<=5:
            task = random.choice(list(self.todolist2))
            each_hour = self.todolist2[str(task)]
            hour += float(each_hour)
            self.finished_percent[task] += self.percent(task)
            max_per = max(self.finished_percent,key=lambda x:self.finished_percent[x])
            min_per = min(self.finished_percent,key=lambda x:self.finished_percent[x])

            if hour<=5.5:
                if (self.finished_percent[max_per]-self.finished_percent[min_per])<=0.2:
                    self.finished_percent[task]+= self.percent(task)
                    rst.append(task)
                else:
                    hour -= float(each_hour)
                    self.finished_percent[task] -= self.percent(task)
                    rst.append(min_per)
                    self.finished_percent[min_per] += self.percent(min_per)
                    hour += float(self.todolist2[str(min_per)])
                    pass
            else:
                hour-=float(each_hour)
                self.finished_percent[task] -= self.percent(task)
                break
        return rst

    def choose_week(self):
        """每周的计划（五天）"""
        all_rst = []
        for i in range(1,6):
            all_rst.append(self.choose_one())
            #print(self.choose_one())
        return all_rst,self.finished_percent

task = Task()
print(task.choose_week())
#print(task.finished_percent)