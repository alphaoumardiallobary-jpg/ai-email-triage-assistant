import os
from dotenv import load_dotenv
from email_parser import analyze_email, save_result
from sample_emails import SAMPLE_EMAILS

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: no se encontró OPENAI_API_KEY en el archivo .env")
        return

    print("AI Email Triage Assistant")
    print("-" * 30)
    print("1. Analizar un email manualmente")
    print("2. Probar con emails de ejemplo")

    option = input("Selecciona una opción (1/2): ").strip()

    if option == "1":
        email_text = input("\nPega el contenido del email:\n> ").strip()
        result = analyze_email(email_text)

        print("\nResultado del análisis:")
        for key, value in result.items():
            print(f"{key}: {value}")

        save_result(result)
        print("\nResultado guardado en outputs/parsed_emails.json")

    elif option == "2":
        for i, email_text in enumerate(SAMPLE_EMAILS, start=1):
            print(f"\n--- Email {i} ---")
            print(email_text)

            result = analyze_email(email_text)

            print("\nResultado del análisis:")
            for key, value in result.items():
                print(f"{key}: {value}")

            save_result(result)

        print("\nTodos los resultados fueron guardados en outputs/parsed_emails.json")

    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()