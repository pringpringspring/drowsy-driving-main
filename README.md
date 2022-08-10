# 🎓졸업작품 - 눈을 이용한 졸음운전 감지 및 자율주행

### 작품 소개
* 졸음운전은 최근 10년간 발생원인별 고속도로 교통사고율의 1위이며 화물차 교통사고의 원인중 과반을 차지한다.
* 이를 사전에 방지하는것이 목적이다.

### 개발 시 기대효과
* 사고율 감소
* 운전습관 교정

### 개발 기간 : 2021.03 ~ 2021.06
### 개발 일정
![0022](https://user-images.githubusercontent.com/93775304/183740403-58a645b1-370a-4aa8-9e58-d9d44b646c05.jpg)
![0023](https://user-images.githubusercontent.com/93775304/183740418-9ded22fb-c190-426a-9fd3-ec701554d91a.jpg)
![0024](https://user-images.githubusercontent.com/93775304/183740430-471bc422-9ae4-4268-b71d-f5ffff298754.jpg)

#
### 개발 기능
#### 1.눈 깜빡임 인식
* openCV와 Harr Cascade 알고리즘 사용
* dlib의 facial landmark 사용
* 실시간으로 눈을 인식하여 좌표를 그린 후 눈의 종횡비(Aspect Ratio)를 계산한다.
* 종횡비가 임계값 미만이면 눈을 감고있다고 판단, 이상이면 눈을 뜨고있는 상태라 판단한다.
* 3초이상 눈을 감고있을때 피에조 부저를 울리게 한다.

#### 2.차선 인식
* openCv와 numpy 사용
* 값이 일정 범위 내라면, 직진으로 판단하여 주행
* 값이 최대속력보다 크다면 좌회전, 작으면 우회전으로 판단
* 차선을 구분하기위해 카메라에서 Grayscale로 변환 및 좌표값 추출
![lane](https://user-images.githubusercontent.com/93775304/183846693-4393a35c-656b-4a58-924a-2df4a0450564.gif)
