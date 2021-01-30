import streamlit as st
import requests
import io#input output
from PIL import Image
from PIL import ImageDraw

#タイトルを入力
st.title('顔認識アプリ')

#
subscription_key = '3f37265fbd31412f95228e6ae16401da'
assert subscription_key
face_api_url = 'https://20210130yamada.cognitiveservices.azure.com/face/v1.0/detect'

#画像をアップロードするコマンド
uploaded_file = st.file_uploader("Choose an image....",type ='jpg')

#変数の中に何か入っていたら
if uploaded_file is not None:
    #Imageのopenメソッド
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output,format='JPEG')
        binary_img = output.getvalue()#binaryデータの取得

    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key':subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses'
    }

    res= requests.post(face_api_url, params=params,headers=headers,data=binary_img)
    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']), (rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green')
    
    st.image(img,caption = 'Uploaded Image.',use_column_width=True)