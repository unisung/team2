import requests
import xml.etree.ElementTree as ET
from ..models import Item
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
import pandas as pd
import logging
# 김건우 tAW=8pgqZ6Tc=y1jE6TwghqJoEJVKdR/0vYDh9e9v4M=
# 함재성님 xc=fNSPlekiRmn9ZzXCGoVGXM0y3hO75W9L3O065IRs=
# 강사님 Ag6oGQJetRsWvgiB52hxwi5Pz0e0TTff/B1veBWZg7M=
# 세인 nd54Dxg1lMZ9KLwgOCj9pIxb7y8qZIHezsCLri2lmQw=
# 현재 데이터 103500개. api 1개당 103500가능하므로 apikey 더 가져와야함. 
# 1000번 호출 제한이므로 numOfRows수를 바꾸면 다 가져올 수 있을듯?
def fetch(request):
    if request.method == 'POST' and 'query' in request.POST:
        api_key = 'xc=fNSPlekiRmn9ZzXCGoVGXM0y3hO75W9L3O065IRs='
        query = request.POST.get('query', '')
        page_no = 1
        more_pages = True
        error_count = 0
        max_errors = 10

        while more_pages:
            try:
                url = f'http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getWordSearch?word={query}&numOfRows=500&pageNo={page_no}&ServiceKey={api_key}'
                response = requests.get(url, timeout=30)
                logging.info(f"API Response Content: {response}")
                
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.content)
                        items = root.findall('.//item')

                        print(type(items))

                        # 데이터 처리 로직...
                        for i in range(len(items)):
                            current_item = items[i]

                            q = Item()
                            q.applicantName = current_item.find('applicantName').text if current_item.find('applicantName') is not None else None
                            q.applicationDate = current_item.find('applicationDate').text if current_item.find('applicationDate') is not None else None
                            q.applicationNumber = current_item.find('applicationNumber').text if current_item.find('applicationNumber') is not None else None
                            q.astrtCont = current_item.find('astrtCont').text if current_item.find('astrtCont') is not None else None                                                       
                            q.bigDrawing = current_item.find('bigDrawing').text if current_item.find('bigDrawing') is not None else None
                            q.drawing = current_item.find('drawing').text if current_item.find('drawing') is not None else None
                            q.indexNo = current_item.find('indexNo').text if current_item.find('indexNo') is not None else None
                            q.inventionTitle = current_item.find('inventionTitle').text if current_item.find('inventionTitle') is not None else None
                            q.ipcNumber = current_item.find('ipcNumber').text if current_item.find('ipcNumber') is not None else None
                            q.openDate = current_item.find('openDate').text if current_item.find('openDate') is not None else None
                            q.openNumber = current_item.find('openNumber').text if current_item.find('openNumber') is not None else None
                            q.publicationDate = current_item.find('publicationDate').text if current_item.find('publicationDate') is not None else None
                            q.publicationNumber = current_item.find('publicationNumber').text if current_item.find('publicationNumber') is not None else None
                            q.registerDate = current_item.find('registerDate').text if current_item.find('registerDate') is not None else None
                            q.registerNumber = current_item.find('registerNumber').text if current_item.find('registerNumber') is not None else None
                            q.registerStatus = current_item.find('registerStatus').text if current_item.find('registerStatus') is not None else None
                            q.save()

                            print(page_no)

                        page_no += 1
                        error_count = 0  # 성공 시 오류 카운트 초기화

                    except ET.ParseError as e:
                        print(f"XML Parsing failed on page {page_no}: {e}")
                        page_no += 1  # XML 파싱 오류 시 다음 페이지로 이동

                else:
                    error_count += 1
                    print(f"Failed to fetch data: {response.status_code}")
                    if error_count >= max_errors:
                        print("Max errors reached, moving to next page.")
                        page_no += 1
                        error_count = 0  # 다음 페이지로 이동 후 오류 카운트 초기화
                    
            except requests.RequestException as e:
                error_count += 1
                print(f"Request failed: {e}")
                if error_count >= max_errors:
                    print("Max network errors reached, moving to next page.")
                    page_no += 1
                    error_count = 0  # 다음 페이지로 이동 후 오류 카운트 초기화

    return render(request, 'Final/test.html')


# # 데이터 중복저장 방지
# def save_item_if_not_exists(application_number, other_data):
#     # get_or_create 메서드를 사용하여 중복 검사 및 저장
#     item, created = Item.objects.get_or_create(applicationNumber=application_number, defaults=other_data)

#     if created:
#         print(f"새로운 Item이 저장되었습니다: {application_number}")
#     else:
#         print(f"Item이 이미 존재합니다: {application_number}")

# # 데이터 리스트 예시
# data_list = [
#     {'applicationNumber': '123', 'applicantName': 'Name1', ...},
#     {'applicationNumber': '456', 'applicantName': 'Name2', ...},
#     # 더 많은 데이터...
# ]

# # 데이터 리스트를 반복하면서 각 항목 저장 시도
# for data in data_list:
#     save_item_if_not_exists(data['applicationNumber'], data)
