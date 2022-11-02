# Codestates_Section3_Project

## Section 3 학습 내용

+ N311 - 개발환경(CLI, python 가상환경, git, github)
+ N312,N313 - SQL
+ N314 - DB API(sqlite3, psycopg2)
+ N321 - Python (class, decorator)
+ N322 - web 스크랩핑(beautifulsoup)
+ N323 - API
+ N324 - NoSQL(NoSQL, JSON, MongoDB)
+ N331 - Docker
+ N332 - Flask(Jinja, Bootstrap)
+ N333 - 배포(Heroku), 대쉬보드(Matabase), WSGI
+ N334 - 시간, 부호화&복호화

## Section 3 Project Requirements

##### To. 데이터 파이프라인 구축
##### By. 구색을 갖춘 서비스 구현(서비스 정의, 추구 가치)
+ DB 구축
  + 데이터 선택
  + 데이터 수집(스크래핑&크롤링 or API)
+ 데이터 저장
+ API 서비스 개발
+ 데이터 분석용 Dash board 개발

+ +α
  + 배포
    + 대쉬보드
    + 플라스크(API 서비스)
  + 동적 스크래핑(Selenium)
  + 서버형 로컬 DB(PostgreSQL, Docker)
  + 스케줄링(윈도우 스케줄러)
  + API 활용 결과의 DB 및 대시보드 반영
  
## 서비스 정의

+ 투자를 위해 주식을 선택할 때, 이를 보조할 추천 서비스 필요.
+ 주식에 대한 기술적 분석의 한 방법인 캔들 분석(basic - 일봉 / advanced - 주봉, 월봉)을 활용(참고 : https://www.skyer9.pe.kr/wordpress/?p=1773)
+ 종목이름 혹은 종목코드를 추천받아, 예상가와 적중 확률(basic - 익일 / advanced - 일주일, 한달 후의 주가)을 출력해주는 웹 페이지 설계

## 특이사항
+ collector.py에 의한 데이터 수집이 불완전 => 수집 기능은 있으나, 사용하지 않음
  + 기존 데이터가 존재함에도 이를 삭제하고, 새로 받아온 데이터로 대체. -> 오래걸림
  + 조회 제한을 위한 3.6초의 간격 설정 시, 데이터 수집 소요 시간이 너무 김
  + 프로젝트 간소화를 위해, 일부 기간의 데이터만 받아오려 했으나, 1985년부터 주식 데이터를 크롤링함
  + => 이후 서비스 개발 등의 과정은 기존에 크롤링 하던 주식 데이터로 대체하여 최근 1년의 주가 데이터로 수행.

## Log

<<<<<<< HEAD
> 2022-11-02 16:05 ~ 17:40 수집한 데이터를 CSV파일로 내보내는 코드 완성   
=======
>>>>>>> fb8ca270ffafe6372ecdc67e7f06adee36c1679e
> 2022-11-02 15:00 ~ 16:05 데이터 수집 코드 완성   
> 2022-11-02 08:30 ~ 10:10 데이터 수집 코드 작성   
> 2022-11-02 00:20 ~ 03:10 데이터 수집 코드 작성   
> 2022-11-01 15:40 ~ 19:20 데이터 수집 코드 작성   
> 2022-11-01 15:00 ~ 15:40 github 연결   
> 2022-11-01 14:45 ~ 15:00 구현 계획 수립   
