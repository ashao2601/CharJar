from PIL import Image, ImageEnhance
from flask import Flask, request, redirect, url_for, render_template
from random import seed,random, randint
import time



image1 = Image.open('sl.png')
image2 = Image.open('sr.png')

shadows = Image.alpha_composite(image1,image2)

image1 = Image.open('il.png')
image2 = Image.open('ir.png')
i = Image.alpha_composite(image1,image2)

image1 = Image.open('le5.png')
image2 = Image.open('re4.png')

e = Image.alpha_composite(image1,image2)

image1 = Image.open('pl3.png')
image2 = Image.open('pr3.png')
p = Image.alpha_composite(image1,image2)


image1 = Image.open('rbl3.png')
image2 = Image.open('rbs3.png')
rb = Image.alpha_composite(image1,image2)

image1 = Image.open('lbl3.png')
image2 = Image.open('lbs3.png')
lb = Image.alpha_composite(image1,image2)
b = Image.alpha_composite(lb, rb)




i1 = Image.open('f2.png')
i2 = Image.open('e.png')
i9 = Image.open('n2.png')
i10 = Image.open('m.png')
im = Image.alpha_composite(i1, i2)
im = Image.alpha_composite(i9, im)
f = Image.alpha_composite(i10, im)

eyes = Image.alpha_composite( i, p )
eyes = Image.alpha_composite( e, eyes )
eyes = Image.alpha_composite( eyes, b )

f = Image.alpha_composite( eyes, f )

f.save('/Users/tobias/Desktop/SD/static/out.png')
