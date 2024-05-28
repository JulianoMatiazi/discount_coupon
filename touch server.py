from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

def create_discount_coupon(name):
    width, height = 768, 768
    background_color = (0, 0, 0)

    image = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_medium = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 30)
        font_bold = ImageFont.truetype("arialbd.ttf", 40)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    main_text = "Você ganhou"
    w, h = draw.textsize(main_text, font=font_large)
    draw.text(((width - w) / 2, 100), main_text, fill="white", font=font_large)

    discount_box_width, discount_box_height = 300, 200
    discount_box_color = (255, 255, 255)
    discount_box_x = (width - discount_box_width) / 2
    discount_box_y = 250

    draw.rectangle(
        [discount_box_x, discount_box_y, discount_box_x + discount_box_width, discount_box_y + discount_box_height],
        fill=discount_box_color
    )

    discount_text_1 = "R$ 50"
    discount_text_2 = "de desconto"

    w1, h1 = draw.textsize(discount_text_1, font=font_bold)
    w2, h2 = draw.textsize(discount_text_2, font=font_medium)

    draw.text(
        ((width - w1) / 2, discount_box_y + 40),
        discount_text_1,
        fill="black",
        font=font_bold
    )
    draw.text(
        ((width - w2) / 2, discount_box_y + 120),
        discount_text_2,
        fill="blue",
        font=font_medium
    )

    small_text = "Cupom válido por tempo\nlimitado e gerado automaticamente."
    w, h = draw.textsize(small_text, font=font_small)
    draw.text(
        ((width - w) / 2, discount_box_y + discount_box_height + 50),
        small_text,
        fill="white",
        font=font_small
    )

    name_box_width, name_box_height = 400, 50
    name_box_color = (255, 255, 255)
    name_box_x = (width - name_box_width) / 2
    name_box_y = 650

    draw.rectangle(
        [name_box_x, name_box_y, name_box_x + name_box_width, name_box_y + name_box_height],
        fill=name_box_color
    )

    name_text = f"Para: {name}"
    w, h = draw.textsize(name_text, font=font_small)
    draw.text(
        (name_box_x + 10, name_box_y + 10),
        name_text,
        fill="black",
        font=font_small
    )

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    
    return buffer

@app.route('/gerar_imagem', methods=['GET'])
def gerar_imagem():
    name = request.args.get('name', 'Usuário')
    img_buffer = create_discount_coupon(name)
    return send_file(img_buffer, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
