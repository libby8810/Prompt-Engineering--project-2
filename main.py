import os
import gradio as gr
from google import genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def translate_to_cli(user_input):
    if not user_input:
        # אם אין קלט, נשאיר את התיבה נסתרת
        return gr.update(visible=False)
    
    try:
        combined_prompt = f"{SYSTEM_PROMPT}\n\nUser Instruction: {user_input}"
        
        response = client.models.generate_content(
            model="gemma-3-4b-it", 
            config={"temperature": 0.0},
            contents=combined_prompt
        )
        
        result = response.text.strip().replace("`", "")
        
        # מחזירים עדכון לרכיב: הערך החדש ושינוי הראות (visible) ל-True
        return gr.update(value=result, visible=True)
        
    except Exception as e:
        return gr.update(value=f"Error: {str(e)}", visible=True)

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 CLI Agent - Smart Interface")
    
    # הסרנו את gr.Row כדי שהרכיבים יהיו אחד מתחת לשני
    with gr.Column():
        gr.Markdown("### 📝 הקלד הוראה להמרה")
        input_text = gr.Textbox(
            label="", 
            placeholder="למשל: מחק את כל קבצי ה-log בתיקיית temp", 
            lines=3
        )
        submit_btn = gr.Button("🚀 המרה ל-CLI", variant="primary")
        
        # הפרדה ויזואלית
        gr.HTML("<br>") 

        # הגדרת התיבה כנסתרת כברירת מחדל (visible=False)
        output_section = gr.Code(
            label="💻 פקודת טרמינל (ניתן להעתקה)",
            language="shell",
            interactive=False,
            visible=False 
        )
    
    # עדכון: ה-outputs מקבל את ה-output_section כולו
    submit_btn.click(
        fn=translate_to_cli, 
        inputs=input_text, 
        outputs=output_section,
        show_progress="full"
    )

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(), 
        css=".gradio-container {direction: rtl;}"
    )