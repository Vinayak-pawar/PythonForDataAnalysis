from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib
import pandas as pd



class ScrapFlipkart:

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        print("Web scrapping www.Flipkart.com for iPhone")


    def __removeTag(self,a):
        b = a.split('>')[1].split('<')[0]
        #b = b.replace('\u20b9','')
        b = b.replace('\xe2\x82\xb9',' ')
        return b

    def __removeTagPrice(self,a):
        b = a.split('>')[1].split('<')[0]
        #b = b.replace('\u20b9','')
        b = b.replace('\xe2\x82\xb9',' ')
        return b
    
    def __dataFetch(self,myUrl):

        priceList=[]
        productList=[]
        ratingLst=[]

        uClient = uReq(myUrl)
        #uClient.add_header('Accept-Encoding', 'utf-8')
        """page_html1 = uClient.read()
    
        page_html = str(page_html1)
        uClient.close()"""


        pageSoup = soup(uClient.read().decode('utf-8', 'ignore'),'html.parser')

        containers = pageSoup.findAll("div",{"class":"_2kHMtA"})

        for i in containers:
            str_price = str(i.findAll("div",{"class":"_30jeq3 _1_WHN1"}))
            str_product = str(i.findAll('div',{'class':'_4rR01T'}))
            str_rating = str(i.findAll("div",{"class":"_3LWZlK"}))

        #priceList.append(str_price)
        #productList.append(str_product)
        #ratingLst.append(float(str_rating))
            #priceList.append(self.__removeTag(str_price))
            priceList.append(self.__removeTag(str_price))
            productList.append(self.__removeTag(str_product))
            ratingLst.append(float(self.__removeTag(str_rating)))

  
        

        df = pd.DataFrame(list(zip(productList, priceList,ratingLst)))
    
    #return list(zip(productList, priceList,ratingLst))
        return df
    


    def get_data(self):
        Urls = 'https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={0}'


        myLst = []

        finalDf = pd.DataFrame()
        for i in range(1,4):
            df2 = pd.DataFrame()
            df2 = self.__dataFetch(Urls.format(i))
            myLst.append(df2)


        finalDf = pd.concat(myLst) 
        finalDf.columns = ['Product Name','Price','Rating']

        return finalDf




#sys.stdin.reconfigure(encoding='utf-8')
#sys.stdout.reconfigure(encoding='utf-8')
#set PYTHONIOENCODING=utf-8
#set PYTHONLEGACYWINDOWSSTDIO=utf-8

Fp = ScrapFlipkart()


df1 = Fp.get_data()


print('**********************************')
print("Flipkart")
print(df1.size)
print(df1.head())