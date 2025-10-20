default_stock = 'AAPL'
financials_api_url = 'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/'
summary_api_url = 'https://query2.finance.yahoo.com/v7/finance/quote'
eps_api_url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'
ofx_api_url = 'https://api.ofx.com/PublicSite.ApiService/OFX/spotrate/Individual/USD/'
yahoo_url = 'https://finance.yahoo.com/quote'
search_url = 'https://query2.finance.yahoo.com/v1/finance/search'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',      
    'Accept': 'application/json',
    'Cookie': 'gam_id=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A; tbla_id=ae1c33c9-968b-4267-acf9-8d840d8251a1-tuctbc9f210; GUC=AQEBCAFliYBltEIeiQSX&s=AQAAAH7EZOHq&g=ZYgwYg; A1=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; A3=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; gpp=DBAA; gpp_sid=-1; axids=gam=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A&dv360=eS1uRzhBUjVaRTJ1RTBabUt6OWdjeDZwRmJhdG5NZ0UyMn5B&ydsp=y-Y2zOWI5E2uLK1Zgb88WuWLWVD3l.xMMh~A; cmp=t=1703656357&j=0&u=1---; PRF=t%3DAMD%252BAAPL%252BBABA%252BTCEHY%26newChartbetateaser%3D0%252C1704775172404; A1S=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4&j=WORLD'
}