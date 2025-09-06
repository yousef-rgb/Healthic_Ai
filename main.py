import requests
import flet as ft 

# --- إعدادات الموديل والـ API ---
MODEL = "deepseek/deepseek-chat-v3-0324"
URL = "https://openrouter.ai/api/v1/chat/completions"


SYSTEM_PROMPT = (
    "أنت مساعد طبي افتراضي ذكي. دورك أن ترد على أسئلة المستخدمين المتعلقة "
    "بأي نوع من الأمراض (حاد أو مزمن). يجب أن تقدم إجابات تشمل: \n"
    "انت عبارة عن مساعد طبي متخصص قادر على الاجابة عن اي سؤال يتعلق باي شيء يخص الطب والادوية بالاضافة الى تشخيص الامراض وطرق علاجها"
    "لو اتسالت مين الي عملك او مين الي صممك او اي سؤال في السياق دا تجاوب بانه يوسف محمد ابراهيم "
    "لو سُئلت عن أي شيء خارج المجال الطبي، رد: 'آسف، لقد صممني يوسف محمد ابراهيم على أن مساعد طبي ولست مخصصًا لهذا المجال.'"
)



API_KEY = "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"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# --- دالة لطلب الإجابة من OpenRouter ---
def ask_openrouter(question, max_tokens=2000, temperature=0.8):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]



# --- واجهة Flet ---
def main(page: ft.Page):
    page.title = "Chronic Diseases Chatbot"
    page.scroll = "auto"
    page.padding = 20
    page.bgcolor = "#f9f9f9"

    chat = ft.Column(spacing=10, expand=True)

    user_input = ft.TextField(
        label="اكتب سؤالك عن الأمراض المزمنة",
        autofocus=True,
        expand=True
    )

    def send_question(e):
        question = user_input.value.strip()
        if not question:
            return

        # عرض السؤال في بطاقة زرقاء
        chat.controls.append(
            ft.Container(
                content=ft.Text(f"You: {question}", size=16, color="white"),
                bgcolor="#4a90e2",
                padding=10,
                border_radius=10,
                alignment=ft.alignment.center_left
            )
        )

        try:
            answer = ask_openrouter(question)
        except Exception as err:
            answer = f"[خطأ] {err}"

        # إزالة ** من النص
        clean_answer = answer.replace("**", "")

        # عرض الإجابة في بطاقة رمادية
        chat.controls.append(
            ft.Container(
                content=ft.Text(f"Bot: {clean_answer}", size=16, color="black"),
                bgcolor="#e6e6e6",
                padding=10,
                border_radius=10,
                alignment=ft.alignment.center_left
            )
        )

        user_input.value = ""
        page.update()

    send_btn = ft.ElevatedButton("إرسال", on_click=send_question)

    page.add(
        chat,
        ft.Row([user_input, send_btn])
    )


ft.app(main)
