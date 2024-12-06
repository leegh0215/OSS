import json

#파일 저장 경로
DO_FILE = "do.json"

#초기 데이터 로드
def load_do():
  try:
    with open(DO_FILE, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    return []

#데이터 저장
def save_do(do_list):
  with open(DO_FILE, 'w') as file:
    json.dump(do_list, file, indent=4)

def main():
  do_list = load_do()
  while True:
    print("\n[체크리스트]")
    print("1. 할 일 목록 보기")
    print("2. 할 일 추가")
    print("3. 할 일 완료 표시")
    print("4. 할 일 삭제")
    print("5. 종료")

    choice = input("메뉴를 선택하세요 : ")
    if choice == "1":
      print("아직 미구현")
    elif choice == "2":
      print("아직 미구현")
    elif choice == "3":
      print("아직 미구현")
    elif choice == "4":
      print("아직 미구현")
    elif choice == "5":
      save_do(do_list)
      print("프로그램을 종료합니다.")
      break
    else:
      print("올바른 메뉴를 선택하세요!")

main()
