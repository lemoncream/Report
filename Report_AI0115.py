import pandas as pd
import numpy as np

class SimpleChatBot:
    def __init__(self, filepath):  # 클래스 초기화하면 load_data 함수를 호출 
        self.questions, self.answers = self.load_data(filepath)   # questions 리스트와 answers 리스트를 각각 questions, answers 변수에 담음
        
    def load_data(self, filepath):
        data = pd.read_csv(filepath)    # csv 파일 불러와 데이터프레임으로 변환하여 data에 담음
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()    # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers       # questions와 answers 리스트 반환

    def calc_distance(self, a, b):      # 레벤슈타인 거리 계산하기
        if a == b: return 0       # 두 문자열이 같으면 0을 반환
        a_len = len(a)            # a 길이를 구해 a_len에 넣음
        b_len = len(b)            # b 길이를 구해 b_len에 넣음
        if a == "": return b_len  # a가 빈 문자열이면 b로 변환하는데 b 길이만큼 비용 필요하므로 레벤슈타인 거리도 b 길이만큼 나옴
        if b == "": return a_len  # b가 빈 문자열이면 a로 변환하는데 a 길이만큼 비용 필요하므로 레벤슈타인 거리도 a 길이만큼 나옴
        # 2차원 표 (a_len+1, b_len+1) 준비하기 
        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 (a길이+1)개 빈 리스트를 가진 리스트 생성
        for i in range(a_len+1):             
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 (b 길이+1)만큼 0을 각 리스트의 요소로 집어넣음
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):           # 각 리스트의 첫번째 요소를 리스트 행 번호와 같은 숫자로 넣음
            matrix[i][0] = i
        for j in range(b_len+1):           # 첫번째 리스트의 각 요소에 인덱스값과 일치하는 숫자를 넣음. 예: [0, 1, 2, 3]
            matrix[0][j] = j
        # 표 채우기
        for i in range(1, a_len+1):                
            ac = a[i-1]                    # a 문자열의 각 글자를 가져다가
            for j in range(1, b_len+1):
                bc = b[j-1]                # b 문자열의 각 글자와 비교하여 
                cost = 0 if (ac == bc) else 1  # 두 문자가 같으면 비용이 0이고 다르면 1
                matrix[i][j] = min([        # 문자 제거, 삽입, 변경 다 해보고 그 중 최소값을 매트릭스에 넣음
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선의 +1. 문자가 동일하면 대각선 숫자 그대로 복사
                ])                         
        return matrix[a_len][b_len]         # 매트릭스 마지막 수를 비용값(편집거리)으로 가져옴
    
    def compare(self, input_sentence):   # 사용자 질문을 인자로 받아 데이터셋의 질문들과 거리를 비교
        
        scores = []          # 거리를 담을 빈 리스트 생성                        
        for q in self.questions:       
            score = self.calc_distance(input_sentence, q)    # 데이터셋의 각 question과 사용자 질문 간의 거리를 계산
            scores.append(score)       # 거리들을 모두 score 리스트에 담음
        array = np.array(scores)       # argmin 함수를 사용하기 위해 리스트를 array로 변환
        best_match_index = array.argmin()  # 거리가 가장 낮은 question의 index 반환  
        return self.answers[best_match_index]   # 해당 index를 가진 answer를 찾아 반환

# 학습데이터셋인 CSV 파일 경로 지정
filepath = 'ChatbotData.csv'

# SimpleChatBot 클래스의 챗봇 객체 생성
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    input_sentence = input('You: ')          # 사용자 질문을 입력받음  
    if input_sentence.lower() == '종료':     # 종료 입력시 break문으로 챗봇 종료
        print('Chatbot has left the room')   # 챗봇이 종료되었음을 알림
        break
    response = chatbot.compare(input_sentence)      # 사용자 질문에 대한 answer를 찾아 반환
    print('Chatbot:', response)              # 챗봇의 답변 출력
     