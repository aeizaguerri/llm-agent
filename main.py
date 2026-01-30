from src.llm import ChatClient
from src.core import Config


def main():
    chat_client = ChatClient()
    print("Bienvenido al chatbot. Escribe 'exit' o 'quit' para salir.")
    while True:
        try:
            user_input = input("Usuario: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Saliendo del chatbot. ¡Hasta luego!")
                break
            messages = [{"role": "user", "content": user_input}]
            response = chat_client.get_response(model=Config.DEFAULT_MODEL, messages=messages)
            print(f"Chatbot: {response.content}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")                

if __name__ == "__main__":
    main()
