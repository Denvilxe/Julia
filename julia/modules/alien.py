import cv2
from julia import tbot
from julia.events import register
import numpy as np
import math
from vcam import vcam,meshGen
import sys
import os
if not os.path.isdir("./dco/"):
    os.makedirs("./dco/")

@register(pattern="^/alien")
async def fun_mirror(event):
    path = "dco"
    reply = await event.get_reply_message()
    lol = await tbot.download_media(reply.media, path)
    file_name = "mirror.jpg"
    await event.reply("aok")
    hehe = path + "/" + file_name
    img = cv2.imread(lol)
    H,W = img.shape[:2]
    fps = 30
    c1 = vcam(H=H,W=W)
    plane = meshGen(H,W)
    plane.Z += 20*np.sin(2*np.pi*((plane.X-plane.W/4.0)/plane.W)) + 20*np.sin(2*np.pi*((plane.Y-plane.H/4.0)/plane.H))
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x,map_y = c1.getMaps(pts2d)
    output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR,borderMode=0)
    output = cv2.flip(output,1)
    out1 = cv2.resize(output,(700,350))
    cv2.imwrite(file_name,out1)
    await tbot.send_file(event.chat_id, file_name)
    for files in (hehe, lol):
        if files and os.path.exists(files):
            os.remove(files)
    hoi = await event.delete()
