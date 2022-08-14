from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image, ImageFont, ImageDraw
import re
import io
from textwrap import wrap


def register(cb):
    cb(MonkeyMod())


class MonkeyMod(loader.Module):
    """Манкизатор"""
    strings = {
        'name': 'Манкизатор',
        'usage': 'Напиши <code>.help Манкизатор</code>',
    }

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def mcmd(self, message):
        """.j <реплай на сообщение/свой текст>"""

        ufr = requests.get("https://github.com/Sad0ff/modules-ftg/raw/master/open-sans.ttf")
        f = ufr.content

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not args:
            if not reply:
                await utils.answer(message, self.strings('usage', message))
                return
            else:
                txt = reply.raw_text
        else:
            txt = utils.get_args_raw(message)
        await message.edit("<b>Обработка....</b>")
        pic = requests.get("https://memepedia.ru/wp-content/uploads/2021/04/qblulgcbrwk-%E2%80%94-kopija.jpg")
        pic.raw.decode_content = True
        img = Image.open(io.BytesIO(pic.content)).convert("RGB")

        W, H = img.size
        # txt = txt.replace("\n", "𓃐")
        text = "\n".join(wrap(txt, 19))
        t = text + "\n"
        # t = t.replace("𓃐","\n")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(io.BytesIO(f), 64, encoding='UTF-8')
        w, h = draw.multiline_textsize(t, font=font)
        imtext = Image.new("RGBA", (w + 50, h + 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(imtext)
        draw.multiline_text((30, 30), t, (255, 255, 255), font=font, align='center')
        imtext.thumbnail((W, H))
        w, h = imtext.size
        img.paste(imtext, ((W - w) // 2, (H - h) // 2), imtext)
        out = io.BytesIO()
        out.name = "out.jpg"
        img.save(out)
        out.seek(0)
        await message.client.send_file(message.to_id, out, reply_to=reply)
        await message.delete()