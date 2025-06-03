from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)  

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# 요리 리스트 정의
cuisines = [
    "", # 기본 빈 값 (선택하지 않았을 때)
    "Italian", "Mexican", "Chinese",
    "Indian", "Japanese", "Thai", "French",
    "Mediterranean", "American", "Greek"
]

# Dietary restriction 목록 추가(생활 방식에 맞는 식이 제한)
dietary_restrictions = [
    "Gluten-Free", "Dairy-Free", "Vegan", "Pescatarian",
    "Nut-Free", "Kosher", "Halal", "Low-Carb",
    "Organic", "Locally Sourced"
]

# create a dictionary to store the languages and their corresponding codes
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi'
}

# Google Gemini API 설정
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')  # 기본 URL('/') 경로에 대한 라우팅
def index():
    # Display the main ingredient input page
    # index.html 템플릿에 cuisines 리스트 전달
    return render_template(
        'index.html',
        cuisines=cuisines,           
        dietary_restrictions=dietary_restrictions,
        languages = languages
    )

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Extract the three ingredients from the user's input
    ingredients = request.form.getlist('ingredient')

    # Extract cuisine and restrictions, and language
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    print('selected_cuisine: ' + selected_cuisine)
    print('selected_restrictions: ' + str(selected_restrictions))
    print('selected_language ' + selected_language)

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."
    
    # 프롬프트 시작
    prompt = f"""Craft a recipe in HTML {selected_language} using \
        {', '.join(ingredients)}. It's okay to use some other necessary ingredients.\
            Ensure the recipe ingredients appear at the top, \
            followed by the step-by-step instructions."""

    # cuisine 추가
    if selected_cuisine:
        prompt += f"\nThe cuisine should be {selected_cuisine}."

    # restrictions 추가 (리스트를 문자열로 변환)
    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f"""The recipe should have the
        following restrictions: 
        
        {', '.join(selected_restrictions)}."""

    # Gemini API 호출
    try:
        response = model.generate_content(prompt)
        recipe = response.text  # Gemini 응답에서 텍스트 추출
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)
