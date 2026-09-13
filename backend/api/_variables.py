import os
from dotenv import load_dotenv

load_dotenv()

default_stock = 'AAPL'
financials_api_url = 'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/'
summary_api_url = 'https://query2.finance.yahoo.com/v7/finance/quote'
eps_api_url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'
ofx_api_url = 'https://api.ofx.com/PublicSite.ApiService/OFX/spotrate/Individual/USD/'
yahoo_url = 'https://finance.yahoo.com/quote'
search_url = 'https://query2.finance.yahoo.com/v1/finance/search'
finviz_url = 'https://finviz.com/quote.ashx'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
    'accept': 'application/json',
    'cookie': 'cf_clearance=fF3MakRFHi18UqVieAxVkRgkO7xzmd74KfFrYaF2e80-1789280763-1.2.1.1-OC6rDd0c4SSBQu63jGkmP0nxCx2N6TH16GwJ_wPmXGwlTKfqZWNtx6mjSIFiRh_.SoMZflBd4X1p9YaIDrSu3nHzGP_oBDnaBctpkoiw4DF3ZM3Y9p_RtLCNSGrE8ApcrLAE2qImZtGxYeUqUyLqQyMz_GO4ZevCGwB9Qxu7ADUPuRDVHOyPVuKXFHU.UuO.tnIuWGQwKhFJZm3SKOmetEGOzmskT6HB57tUEmbNdgocnl.NU.mUAP0PrPt_iTz.TWMLqIYbhkdHbTLwQ5osOzhcEWjPyL0Vp4AYOA6.WzfJcc91AFNc1PEd4nAIIlU5cz4M.dF4HiqKN_4bwWOTIBgXEeUvzoVoZsYhYd_6PuQ.J0dlWDnxqGUmjMzeXB9EZyn_cHZ3GxkO0oCpYtnb.TfQsPwwNk7psgOq7Wj9Nu7mAmyh4lHeTnrDJq2jDhnxZdbJXViJaxaB6h3eW1RCMAoJP8U0MLRpjNCc8hPVoMljIYQ20ZWJ8qYrsjtkx3Co_pzhLumi7n4R0KvXv78CVw;gam_id=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A; tbla_id=ae1c33c9-968b-4267-acf9-8d840d8251a1-tuctbc9f210; GUC=AQEBCAFliYBltEIeiQSX&s=AQAAAH7EZOHq&g=ZYgwYg; A1=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; A3=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4; gpp=DBAA; gpp_sid=-1; axids=gam=y-TjEDJPZE2uK4i9QlUnuBYCL0ic4L15gV~A&dv360=eS1uRzhBUjVaRTJ1RTBabUt6OWdjeDZwRmJhdG5NZ0UyMn5B&ydsp=y-Y2zOWI5E2uLK1Zgb88WuWLWVD3l.xMMh~A; cmp=t=1703656357&j=0&u=1---; PRF=t%3DAMD%252BAAPL%252BBABA%252BTCEHY%26newChartbetateaser%3D0%252C1704775172404; A1S=d=AQABBCVi3WACEIUwHsGub3w6lx5fuudrkAsFEgEBCAGAiWW0Za-0b2UB_eMBAAcIJWLdYOdrkAs&S=AQAAAhJfv3S_GzYP5xLa4zsXGW4&j=WORLD',
    "content-type": "application/json",
    "referer": "https://finviz.com/",
}
proxies = {
    "http": os.getenv("WEBSHARE_HTTP"),
    "https": os.getenv("WEBSHARE_HTTPS")
}