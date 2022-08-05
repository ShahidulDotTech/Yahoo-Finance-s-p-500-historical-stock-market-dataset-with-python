from email import header
import scrapy

# header to dictonary
def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d


class Spider1Spider(scrapy.Spider):
    name = 'spider1'

    url = 'https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC'
    def start_requests(self):
        h = get_headers(
            '''
            accept: */*
            accept-encoding: gzip, deflate, br
            accept-language: en-US,en;q=0.9
            content-length: 2253
            content-type: application/x-www-form-urlencoded; charset=UTF-8
            cookie: A1=d=AQABBGza7GICEBDrpZRBLhvOntc1Lh6Lc10FEgEBAQEr7mL2YgAAAAAA_eMAAA&S=AQAAAqjtvKrC9fBux4SE_SQURQQ; A3=d=AQABBGza7GICEBDrpZRBLhvOntc1Lh6Lc10FEgEBAQEr7mL2YgAAAAAA_eMAAA&S=AQAAAqjtvKrC9fBux4SE_SQURQQ; A1S=d=AQABBGza7GICEBDrpZRBLhvOntc1Lh6Lc10FEgEBAQEr7mL2YgAAAAAA_eMAAA&S=AQAAAqjtvKrC9fBux4SE_SQURQQ&j=WORLD
            origin: https://finance.yahoo.com
            referer: https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC
            sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Windows"
            sec-fetch-dest: empty
            sec-fetch-mode: cors
            sec-fetch-site: same-site
            user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
            '''
        )
        url = r'https://finance.yahoo.com/quote/%5EGSPC/history?period1=-1325635200&period2=1659657600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
        yield scrapy.Request(url, headers = h)


    def parse(self, response):
        for item in response.css('[data-test="historical-prices"] tbody tr'):
            yield {
                'Date': item.css(':nth-child(1) ::text').get(),
                'Open': item.css(':nth-child(2) ::text').get(),
                'High': item.css(':nth-child(3) ::text').get(),
                'Low': item.css(':nth-child(4) ::text').get(),
                'Close*': item.css(':nth-child(5) ::text').get(),
                'Adj Close**': item.css(':nth-child(6) ::text').get(),
                'Volume': item.css(':nth-child(7) ::text').get(),
            }

# [data-test="historical-prices"] tbody td span