# Porn

> 学习爬虫用的。。爬有意思一点的网站，会比较有动力。。

> 采用scrapy+mongodb+schedule+subprocess，可以配置使用supervisor来进行控制

### 使用

`scrapy crawlall`进行所有的爬虫全量爬取
`scrapy crawlall -i`进行所有的爬虫增量爬取

### 功能
1. 可以解析在线mp4的时长信息
> 分辨率和fps个人觉得在这个项目里没什么用。同一个地址请求次数过多可能会被ban，影响爬虫效率。而一次把moov都请求下来，可能会有好几mb大小，同样影响爬虫的效率。
> 实在有需求的话推荐使用construct，参考![此项目](https://github.com/amarghosh/mp4viewer)


