#main.py
from sales_bot import get_seller_answer

if __name__ == "__main__":
   if __name__ == "__main__":
    history_user = []
    history_manager = []
    history_chat = []

    while True:
        user_message = input()  # Запрашиваем сообщение от пользователя

        if user_message.lower() in ["выход", "exit", "quit"]:
            print("Chat closed")
            break

        response = get_seller_answer(
            history_user=history_user + [user_message],
            history_manager=history_manager,
            history_chat=history_chat + [user_message]
        )

        print( response)

        # Добавляем сообщение в историю чата
        history_user.append(user_message)
        history_chat.append(user_message)
        history_chat.append(response)