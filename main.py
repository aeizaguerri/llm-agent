from dotenv import load_dotenv
from src.chat import ChatClient

load_dotenv()

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
            response = chat_client.get_response(model="openai/gpt-oss-120b:fastest", messages=messages)
            print(f"Chatbot: {response.content}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")                

if __name__ == "__main__":
    main()
