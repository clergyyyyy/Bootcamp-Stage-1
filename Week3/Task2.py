import requests as rq
from bs4 import BeautifulSoup as BS

# PTT Stock URL
URL = 'https://www.ptt.cc/bbs/Stock/index1.html'

# 抓取3頁的文章清單
for round in range(3):
    RES = rq.get(URL)
    
    # 將 HTML 網頁程式碼丟入 bs4 分析模組
    soup = BS(RES.text, 'html.parser')
    
    # 查找文章標題的 HTML 元素
    articles = soup.select('div.r-ent')  # 文章的外層結構
    
    # 查找 "下一頁" 的連結
    paging = soup.select('div.btn-group-paging a')
    next_URL = 'https://www.ptt.cc' + paging[2]['href']
    URL = next_URL  # 進入下一頁的 URL
    
    # 萃取標題、連結和推文數
    for article in articles:
        # 標題
        title_tag = article.select_one('div.title a')
        if title_tag:
            title = title_tag.text.strip()  # 文章標題
            article_url = 'https://www.ptt.cc' + title_tag['href']  # 文章 URL
        else:
            title = "本文已被刪除"
            article_url = "無法取得連結"
        
        # 推文數
        nrec_tag = article.select_one('div.nrec span')
        if nrec_tag:
            nrec = nrec_tag.text.strip()  # 推文數值
        else:
            nrec = "0"  # 若沒有推文數則設為 0
        
        # 發送 GET 請求到內頁以獲取發佈時間
        if article_url != "無法取得連結":
            article_res = rq.get(article_url)
            article_soup = BS(article_res.text, 'html.parser')
            
            # 發佈時間
            meta_values = article_soup.select('div.article-metaline span.article-meta-value')
            if len(meta_values) >= 3:
                publish_time = meta_values[2].text  # 發佈時間
            else:
                publish_time = "無法取得發佈時間"
        else:
            publish_time = "無法取得發佈時間"
        
        # 輸出
        print(f"標題: {title}")
        print(f"推文數: {nrec}")
        print(f"連結: {article_url}")
        print(f"發佈時間: {publish_time}")
        print('-' * 50)
