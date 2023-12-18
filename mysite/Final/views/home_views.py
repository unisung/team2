from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
import pandas as pd
from ..models import Item
import csv
from django.db.models import Q

from sklearn.feature_extraction.text import CountVectorizer

from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone

# home 을 홈 화면으로 사용
def home(request):
    return render(request, 'Final/home.html')

def result(request):
    context = {}
    if request.method == 'POST' and 'keyword' in request.POST:
        keyword = request.POST.get('keyword', '')
        context = {'keyword': keyword}

        # 데이터베이스에서 astrtCont 및 inventionTitle 필드에서 키워드에 해당하는 데이터를 검색
        # all > 모두, filter > 몇개만, get > 
        items_from_db = Item.objects.filter(
            Q(astrtCont__icontains=keyword) | Q(inventionTitle__icontains=keyword)
        )
        if items_from_db.exists():  # 검색 결과가 있는 경우
            # Pandas DataFrame으로 변환
            items_df = pd.DataFrame.from_records(items_from_db.values())
            # 필요한 열만 선택
            items_df = items_df[['inventionTitle', 'astrtCont', 'ipcNumber','registerStatus','applicantName','applicationDate','applicationNumber']]
            columns_order = ['inventionTitle', 'astrtCont', 'ipcNumber','registerStatus','applicantName','applicationDate','applicationNumber']
            items_df = items_df[columns_order]



            # IPC 섹션 계산 및 기타 필요한 데이터 처리
            if not items_df.empty:
                items_df['IPC_Section'] = items_df['ipcNumber'].str.extract(r'([A-H])')
                ipc_section_counts = items_df['IPC_Section'].value_counts()
                ipc_section_counts_df = ipc_section_counts.reset_index()
                ipc_section_counts_df.columns = ['IPC_Section', 'Count']

                context['ipc_section_counts'] = ipc_section_counts_df
                context['ipc_section_counts_list'] = ipc_section_counts_df.values

                # 상위 신청인 정보
                applicant_counts = items_df['applicantName'].value_counts().head(10)
                context['top_applicants_data'] = applicant_counts.to_dict()
                context['top_applicants_data_items'] = applicant_counts.items()

                # context['items'] = items_df  # 결과를 딕셔너리로 변환
                # DataFrame을 HTML로 변환 (DataTables와 호환되도록)
                # context['items_html'] = items_df.to_html(classes='display', id='myDataTable', index=False)
                # DataFrame을 HTML로 변환 (id는 추후에 추가)
                # Pandas DataFrame을 HTML로 변환
                items_html = "<table id='myDataTable' class='display'>"

                # 컬럼 이름으로 테이블 헤더 생성
                items_html += "<thead><tr>"
                for col in items_df.columns:
                    items_html += f"<th>{col}</th>"
                items_html += "</tr></thead>"

                # 데이터 행 생성
                items_html += "<tbody>"
                for index, row in items_df.iterrows():
                    items_html += "<tr>"
                    for item in row:
                        items_html += f"<td title='{item}'>{item}</td>"
                    items_html += "</tr>"
                items_html += "</tbody></table>"

                # 컨텍스트에 추가
                context['items_html'] = items_html
            return render(request, 'Final/result.html', context)

        else:  # 검색 결과가 없는 경우
            context['no_results'] = True
            context['message'] = '조회되는 데이터가 없습니다.'

    return render(request, 'Final/result2.html', context)


        
def download_csv(request):
    keyword = request.GET.get('keyword', '')

    # 데이터베이스에서 'astrtCont' 또는 'inventionTitle' 필드에 키워드가 포함된 항목을 조회
    queryset = Item.objects.filter(
        Q(astrtCont__icontains=keyword) | Q(inventionTitle__icontains=keyword)
    )

    # 쿼리셋을 DataFrame으로 변환
    df = pd.DataFrame.from_records(queryset.values())

    # 정확한 콘텐츠 타입을 가진 HTTP 응답 준비
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{keyword}_data.csv"'

    # UTF-8 인코딩과 BOM 추가
    response.write(u'\ufeff'.encode('utf8'))

    # DataFrame이 비어 있지 않은 경우 CSV로 작성
    if not df.empty:
        writer = csv.writer(response)
        writer.writerow(df.columns)  # 헤더 작성
        for index, row in df.iterrows():
            writer.writerow(row)

    return response