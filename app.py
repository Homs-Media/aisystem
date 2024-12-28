import llamaapi
import json
import google.generativeai as genai
from openai import OpenAI
from flask import Flask , request



#Lama Ai ------------------------------------------------------------------------


def getAnswerFromLama(command , model = "llama3.3-70b") :

    # المفتاح
    llama_api = llamaapi.LlamaAPI("LL-Kh5cPhctRsGTXKlZJp7JC26YQb5OV15xD5hE9iommrskvdjVRvND7l59eegF85fG")

    # النماذج المدعومة
    lama_models = {"llama3.3-70b" , "llama3.2-90b-vision" , "llama3.2-11b-vision" , "llama3.2-3b" , "llama3.2-1b" , "llama3.1-405b" , "llama3.1-70b" , "llama3.1-8b" , "llama3-70b" , "llama3-8b"}

    # تصحيح اسم المودل في حالة اعطاء اسم خاطئ
    if not model in lama_models :
        model = "llama3.3-70b"

    # تحضير الطلب
    api_request_json = {
        "model": model,
        "messages": [
            {"role": "user", "content": command},
        ]
    }

    # ارجاع الناتج عن الطلب
    response = llama_api.run(api_request_json)
    return ((json.loads((json.dumps(response.json(), indent=2)))['choices'][0]['message']['content']))





# Gemini ------------------------------------------------------------------------


def getAnswerFromGemini(command , type = None , model = "gemini-1.5-flash") :

    # ضبط المفتاح
    genai.configure(api_key="AIzaSyBq1_-NMOrWCRWrdHs3HZFL-ErX6I4n0Es")

    # قائمة المودلات
    gemini_models = ["gemini-2.0-flash-exp" , "gemini-1.5-flash" , "gemini-1.5-flash-8b" , "gemini-1.5-pro" , "gemini-1.0-pro"]
    
    #تصحيح اسم المودل في حالة اعطاء اسم مودل غير صحيح
    if not model in gemini_models :
        model = "gemini-2.0-flash-exp"

    # ضبط المودل
    model_hand = genai.GenerativeModel(
        model_name  = model,
        system_instruction=type
    )

    # ارسال الطلب
    response = model_hand.generate_content( command )

    # ارجاع الطلب
    return response.text





#GPT 4 ------------------------------------------------------------------------


def getAnswerFromGpt4(command):
    # ضبط المفتاح
    client = OpenAI(
        api_key="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"
    )

    # ارسال الطلب
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content":command}
        ]
    )

    # ارجاع ناتج الطلب
    return completion.choices[0].message.content





# التطبيق ------------------------------------------------------------------------


app = Flask(__name__)

#صفحة الجيمني
@app.route("/gemini" , methods=["GET"])
def gemini_page() :

    # المدخل
    text = request.args.get("text")

    # التخصيص
    type_in = request.args.get("type")
 
    # المودل
    model_in = request.args.get("model")

    # عرض الناتج
    return getAnswerFromGemini(content = text , type = type_in , model = model_in)
    

#صفحة لاما
@app.route("/lama" , methods=["GET"])
def lama_page() :
    
    # المدخل
    text = request.args.get("text")

    # المودل
    model = request.args.get("model")
  
    # عرض الناتج
    return getAnswerFromLama(text , model)
    

#صفحة جي بي تي
@app.route("/gpt" , methods=["GET"])
def gpt_page() :
 
    # المدخل
    text = request.args.get("text")
  
    # عرض الناتج
    return getAnswerFromGpt4(text)


app.run(debug=True)
