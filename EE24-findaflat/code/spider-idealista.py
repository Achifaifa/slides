import geocoder, scrapy

class MySpider(scrapy.Spider):
  name='idealista'
  allowed_domains=["idealista.com"]
  start_urls=['https://www.idealista.com/alquiler-viviendas/bilbao-vizcaya/']

  def parseflat(self,response):

    size=""
    orientation=""
    rooms=""
    misc_data_flat=response.xpath("//*[@id='details']/div[4]/ul/*/text()").extract()
    for i in misc_data_flat:
      if u"m²" in i: size=i
      if u"Orientación" in i: orientation=i
      if "habitaciones" in i: rooms=i

    floor=""
    int_ext=""
    lift=""
    misc_data_bldg=response.xpath("//*[@id='details']/div[5]/ul/*/text()").extract()
    for i in misc_data_bldg:
      if "Planta" in i: floor=i
      if "interior" in i: int_ext="interior"
      if "exterior" in i: int_ext="exterior"
      if "ascensor" in i: lift=i

    addr_approx=response.xpath("//*[@id='main-info']/h1/span/text()")[0].extract().split(' en ')[-1]
    geodata=geocoder.google(addr_approx)
    gps=geodata.latlng
    cp=geodata.postal
    publicdistance="?"
    
    price=response.xpath("//*[@id='details']/div[2]/ul/li[1]/text()")[0].extract()
    contact=response.xpath("//*[@class='contact-phones']/*/p/text()").extract()
    pics=response.xpath("//img/@src").extract()
    deposit=response.xpath("//*[@id='details']/div[2]/ul/li[1]/text()")[0].extract()
    description=response.xpath("//*[@class='commentsContainer']/div/text()")[0].extract()

    return {'sku':sku, 'name':name, 'price':price, 'type':cubetype}

  def parse(self,response):

    flats=[i for i in a if "/inmueble/" in response.xpath("//a/@href").extract()]

    for flat in flats:
      flaturl=response.urljoin(cube)
      yield scrapy.Request(flaturl,callback=self.parseflat)
    
    nexturl=response.xpath('//*[@class="next"]/a/@href').extract()
    if nexturl: nexturl=response.urljoin(nexturl[0])
    yield scrapy.Request(nexturl, callback=self.parse)
