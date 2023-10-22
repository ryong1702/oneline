from typing import Union
import pandas as pd
from fastapi import FastAPI
import pandas as pd
from datetime import datetime
import const.query as query
from sqlalchemy import create_engine

app = FastAPI()
engine = create_engine("postgresql://postgres:postgres@oneline.net:5432/companyfiling")

@app.get("/company")
def getCompany():
    """
    # company 데이터
    - cik 또는 ticker를 확인하기 위한 API
    
    ## 출력 데이터
    - **cik**: 기업 번호(예:0000001800)
    - **ticker**: 기업 티커(예:ABT)
    - **name**: 기업 이름
    - **exchange**: 거래소 이름
    """
    return pd.read_sql(sql=query.GET_COMPANY, con=engine).to_dict('records')

@app.get("/finance/{company}")
async def getFinance(company:str, fileType:Union[str, None]='ALL', startDate:Union[str, None]='2010-01-05',
 endDate:Union[str,None]=datetime.today().strftime('%Y-%m-%d'), dataType:Union[str,None]="sent"):
    """
    # finance 데이터
      - company(0000001800(cik) 또는 ABT(기업 티커)), fileType(ALL 또는 10-K, 또는 10-Q), 시작날짜, 끝 날짜, dataType 를 입력하여,
      입력 값에 따라서 데이터를 추출하여, 날짜와 텍스트 정보를 표시(100자만 표시)

    # 입력 데이터
    - **company**: cik 또는 ticker를 입력.(**※필수 입력값**)
    - **fileType**: ALL 또는 10-K, 10-Q를 입력.(기본값: ALL, 입력값이 없는 경우는 ALL로 지정)
    - **startDate**: 검색하고 싶은 시작 날짜(기본값: DB에 입력되어 있는 처음 날짜(2010-01-05))
    - **endDate**: 검색하고 싶은 끝 날짜(기본값: 오늘 날짜)
    - **dataType**: sent 또는 token 을 입력(기본값: sent)

    # 입력 예시
    - **company**: AAPL
    - **fileType**: ALL
    - **startDate**: 2012-01-01
    - **endDate**: 2020-12-31
    - **dataType**: token

    # 출력 데이터
    - **date**: 최근 순으로 검색된 날짜를 출력
    - **sentence 또는 token(stop)**:
        - **sentence**: 검색된 데이터를 100자까지 출력(dataType이 token이외의 경우는 sentence로만 출력)
        - **token(stop)**: 검색된 데이터를 소문자로 100자까지 출력(dataType이 token인 경우 출력)
    """
    try:
        isFileType = True if fileType == None or fileType.upper() == 'ALL' else False
        isDataType = True if dataType == 'token' else False
        dataType = 'token(stop)' if isDataType else 'sentence'

        if endDate == None:
            endDate = datetime.today().strftime('%Y-%m-%d')

        if startDate == None:
            df = pd.read_sql(query.GET_START_DATE, con=engine)
            startDate:str = df['fileddate'][0]    

        df = selectDataAll(company, startDate, endDate, dataType) if isFileType else selectDataType(company, fileType, startDate, endDate, dataType)
        result = setLower(df) if isDataType else df.to_dict('records')
        return resultSuccess(result) if result else resultEmptyMessage()
    except Exception as e:
        return dict(result="Error", message=f"{e} 에러가 발생하였습니다.")

def selectDataAll(company, startDate, endDate, dataType):
    return pd.read_sql(query.GET_DATA_ALL.format(ticker=company, cik=company, startDate=startDate, endDate = endDate, dataType=dataType), con=engine)

def selectDataType(company, fileType, startDate, endDate, dataType):
    return pd.read_sql(query.GET_DATA_TYPE.format(ticker=company, cik=company, fileType=fileType, startDate=startDate, endDate = endDate, dataType=dataType), con=engine)

def setLower(df):
    df['token(stop)'] = df['token(stop)'].str.lower()
    return df.to_dict('records')

def resultEmptyMessage():
    return dict(result="Empty", message="결과가 존재하지 않습니다. 검색조건을 다시 지정하세요.", oneline='')

def resultSuccess(result):
    return dict(result='success', message='', oneline=result)