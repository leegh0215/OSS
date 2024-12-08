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
  with open(DO_FILE, 'w', encoding='UTF-8') as file:
    json.dump(do_list, file, indent=4, ensure_ascii=False)

#데이터 추가
def add_do(do_list):
    task = input("추가할 할 일을 입력하세요: ")
    do_list.append({"task": task, "done": False})
    print(f"'{task}' 추가 완료!")

def print_list(do_list):
   if not do_list:
        print("할 일이 없습니다!")
   else:
        print("\n[현재 할 일 목록]")
        for index, item in enumerate(do_list, start=1):
            status = "✔ 완료" if item["done"] else "❌ 미완료"
            print(f"{index}. {item['task']} - {status}")

def delete_do(do_list):
    print_list(do_list)
    try:
        choice = int(input("삭제할 할 일 번호를 입력하세요: "))
        if 1 <= choice <= len(do_list):
            removed_task = do_list.pop(choice - 1)
            print(f"'{removed_task['task']}'가 삭제되었습니다!")
        else:
            print("유효하지 않은 번호입니다.")
    except ValueError:
        print("숫자를 입력하세요.")


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
      print_list(do_list)
    elif choice == "2":
      add_do(do_list)
    elif choice == "3":
      print("아직 미구현")
    elif choice == "4":
      if len(do_list) > 0:
        delete_do(do_list)
      else:
        print("할 일을 추가하세요.")
    elif choice == "5":
      save_do(do_list)
      print("프로그램을 종료합니다.")
      break
    else:
      print("올바른 메뉴를 선택하세요!")

main()
