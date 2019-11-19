# Project: 利用Python进行豆瓣互联网书籍的爬取与分析

### Date: 2019-08-23  

### Author: huiyanglu  

#### Content:    
  
运用requests爬取豆瓣互联网分类下的所有书籍信息，包括书名、作者、ID、打分人数、分数等。  
  
分析内容包括：  

1.打分人数Top 10  
  
2.评分人数大于100且分数最高的互联网书籍Top 10  
  
3.评分人数小于500且分数最高的互联网书籍Top 10  
  
4.作品最多的作者Top 10  

---
#### Updated in 2019-08-27:  
  
douban_internet_bk.py  

爬虫代码，爬取豆瓣互联网分类下的所有999本书的信息。  
  
douban_analysis.ipynb  

jupyter notebook代码，对爬取的数据进行分析的过程。