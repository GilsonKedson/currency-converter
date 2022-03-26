import requests
from bs4 import BeautifulSoup

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ConverterViewSet(APIView):
    ACCEPTED_CURRENCIES = ['USD','EUR', 'BRL']
    
    def get(self, request, format=None):
        currency_base = request.GET.get('currency_base').upper()
        currency_secondary = request.GET.get('currency_secondary').upper()
        amount = request.GET.get('amount')

        if not currency_base or not currency_secondary or not amount:
            return Response("Parâmetros de conversão não foram passados.", status=status.HTTP_204_NO_CONTENT)
        elif not currency_base in self.ACCEPTED_CURRENCIES or not currency_secondary in self.ACCEPTED_CURRENCIES:
            return Response("Moeda não suportada.", status=status.HTTP_204_NO_CONTENT)

        context = {
            'result': self.get_amount_currency(
                currency_base, 
                currency_secondary, 
                amount
            )
        }
    
        return Response(context, status=status.HTTP_200_OK)
    
    
    def get_amount_currency(self, base, secondary, amount) -> float:
        request_page = requests.get('https://pt.exchange-rates.org/')
        soup = BeautifulSoup(request_page.text, 'html.parser')
        
        DOLAR = self.ACCEPTED_CURRENCIES[0]
        EURO = self.ACCEPTED_CURRENCIES[1]
        REAL = self.ACCEPTED_CURRENCIES[2]
        
        amount = float(amount)
        
        if base == DOLAR:
            if secondary == EURO:
                amount_base = soup.find_all('tr')[3]
                amount_secondary = amount_base.find_all('td')[2].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            elif secondary == REAL:
                amount_base = soup.find_all('tr')[3]
                amount_secondary = amount_base.find_all('td')[1].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            else:
                return amount
            
        elif base == EURO: 
            if secondary == DOLAR:
                amount_base = soup.find_all('tr')[2]
                amount_secondary = amount_base.find_all('td')[3].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            elif secondary == REAL:
                amount_base = soup.find_all('tr')[2]
                amount_secondary = amount_base.find_all('td')[1].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            else:
                return amount
            
        else: # REAL
            if secondary == DOLAR:
                amount_base = soup.find_all('tr')[1]
                amount_secondary = amount_base.find_all('td')[3].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            elif secondary == EURO:
                amount_base = soup.find_all('tr')[1]
                amount_secondary = amount_base.find_all('td')[2].getText()[:8]
                return self.calculate_currency(amount, amount_secondary)
            else:
                return amount
            
    
    def casting_replace(self, currency):
        return float(currency.replace(',', '.'))
    
    
    def calculate_currency(self, amount, currency):
        return round(amount * self.casting_replace(currency), 2)
    