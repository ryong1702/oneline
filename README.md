# oneline API 기동순서
1. oneline.zip 파일을 해제
2. VSC(Visual Studio Code)로 oneline.zip 해제한 폴더로 열기
3. 상단의 메뉴바에서 터미널(T)에서 새터미널을 열기
4. 터미널에서 docker-compose build 명령어로 도커 이미지 생성
5. docker images 명령어로 이미지가 생성되었는지 확인.
6. 이미지 생성되었으면, docker-compose up -d 명령어로 도커 이미지 실행
7. docker ps 명령어로 API가 기동되었는지 확인.
8. 외부접속을 위해서, 포트포워딩 설정을 8000번 포트로 설정.


# oneline
- 원하는 기업의 filing을 Pandas DataFrame으로 불러와 분석에 사용 
- 지원 하는 기업 : Nasdaq 5239개, NYSE 4099개 기업 (2022.07.04 기준)
- 지원 하는 파일: 10-K, 10-Q

Parameters: 
    - company (str) : Ticker or CIK code
    - file_type (str, optional) : ’10-K’ or ’10-Q’, If ‘All’, ’10-K’ and ’10-Q’ are called both.
    - start_date (str, optional) : used in combination with end_date. yyyy-mm-dd. Default - first filing date.
    - end_date (str, optional) : used in combination with start_date and same format as start_date. Default - today.
    - data_type (str, optional) :  
        - ‘sent’ (default) : sentences separated by periods.
        - ‘token’ : tokenized lower case words form sentences.