from PIL import Image, ImageEnhance
from flask import Flask, request, redirect, url_for, render_template
from random import seed,random,randint
import os
import time

app = Flask(__name__)

t = 3
fr = 3
i = 3
ya = 3
count = 1
addr = "output"+str(count)+".png"

def ReduceOpacity(i1, opacity):
    """
    Returns an image with reduced opacity.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879
    """
    assert opacity >= 0 and opacity <= 1
    if i1.mode != 'RBGA':
        im = i1.convert('RGBA')
    else:
        im = i1.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.3)
    im.putalpha(alpha)
    return im

@app.route('/')
def index():
    return render_template('index.html', Trust = t, Friend = fr, Int = i, YA = ya, file = "out.png")

@app.route('/generate',methods = ['POST'])
def generate():
    seed(time.clock())
    global addr, count
    
    if os.path.exists("/Users/tobias/Desktop/SD/static/" + addr):
        os.remove("/Users/tobias/Desktop/SD/static/" + addr)
    t = int(request.form['Trust'],10) - 3
    i = int(request.form['Int'],10) - 3
    fr = int(request.form['Friend'],10) - 3
    ya = int(request.form['YA'],10) - 3

    addr = "output"+str(count)+".png"

    image1 = Image.open('sl.png')
    image2 = Image.open('sr.png')
    new = Image.open('out.png')
    new.save('/Users/tobias/Desktop/SD/static/'+addr)

    # choose FACE
    a = randint(1,3)
    c = random() * i
    c = round(c, 1)

    a = c + a

    if a > 3: a = 3
    elif a < 1: a = 1

    temp = int(a)
    string = str(temp)

    i1 = Image.open('f' + str(temp) + '.png')
    i2 = Image.open('e.png')

    # choose NOSE
    if i == 0:
        x = 2

    elif i == -2:
        x = 1

    elif i == 2:
        x = 3

    elif i == -1:
        x = randint(1,2)

    else:
        x = randint(2,3)

    i9 = Image.open('n' + str(x) + '.png')


    # edit MOUTH
    i10 = Image.open('m.png')

    x = 1 + (random() * fr / 10)
    n = int(1145*x)
    j = int(1138*x)
    i10 = i10.resize((n,j))

    # reposition features
    if temp == 1:
        # mouth
        t1 = 1
        t2 = 0
        t3 = 0  #left/right (i.e. 5/-5)
        t4 = 0
        t5 = 1
        t6 = int( (860*x)+278-j ) * -1 + int(25*x)#up/down (i.e. 5/-5)
        i10 = i10.transform(i10.size, Image.AFFINE, (t1, t2, t3, t4, t5, t6))

        # nose
        t1 = 1
        t2 = 0
        t3 = 0  #left/right (i.e. 5/-5)
        t4 = 0
        t5 = 1
        t7 = 27 #up/down (i.e. 5/-5)
        i9 = i9.transform(i9.size, Image.AFFINE, (t1, t2, t3, t4, t5, t7))


    elif temp == 3:
        #mouth
        t1 = 1
        t2 = 0
        t3 = 0  #left/right (i.e. 5/-5)
        t4 = 0
        t5 = 1
        t6 = int( (860*x)+278-j ) * -1 - int(20*x) #up/down (i.e. 5/-5)
        i10 = i10.transform(i10.size, Image.AFFINE, (t1, t2, t3, t4, t5, t6))

        # nose
        t1 = 1
        t2 = 0
        t3 = 0  #left/right (i.e. 5/-5)
        t4 = 0
        t5 = 1
        t7 = -30 #up/down (i.e. 5/-5)
        i9 = i9.transform(i9.size, Image.AFFINE, (t1, t2, t3, t4, t5, t7))


    t1 = int((1145-n)/2)
    t2 = int((1138-j)/2)

    im = Image.alpha_composite(i1, i2)
    im = Image.alpha_composite(i9, im)
    im.paste(i10, (t1,t2), i10.convert("RGBA"))
    f = im




    # choose BROW
    if ya > 0:
        a = randint(1,6)
        c = random() * ya * 1.5
        c = round(c, 1)

        a = c + a

        if a > 6: a = 6
        elif a < 1: a = 1

        a = int(a)

        i5 = Image.open('rbs' + str(a) + '.png')
        i6 = Image.open('rbl' + str(a) + '.png')

        i3 = Image.open('lbs' + str(a) + '.png')
        i4 = Image.open('lbl' + str(a) + '.png')
    elif ya < 0:
        a = randint(1,6)
        c = random() * ya * 1.5
        c = round(c, 1)

        a = a + c

        if a > 6: a = 6
        elif a < 1: a = 1

        a = int(a)

        i5 = Image.open('rbs' + str(a) + '.png')
        i6 = Image.open('rbl' + str(a) + '.png')

        i3 = Image.open('lbs' + str(a) + '.png')
        i4 = Image.open('lbl' + str(a) + '.png')

    else:
        a = 3
        i5 = Image.open('rbs' + str(a) + '.png')
        i6 = Image.open('rbl' + str(a) + '.png')
        i3 = Image.open('lbs' + str(a) + '.png')
        i4 = Image.open('lbl' + str(a) + '.png')


    o = randint(0,7)
    o = o + fr*random()*3

    if o > 7: o = 7
    elif o < 0: o = 0

    o = float(10 -o)
    o = float(o/10)


    i3 = ReduceOpacity( i3, o )
    i5 = ReduceOpacity( i5, o )

    rb = Image.alpha_composite(i6, i5)
    rb = Image.alpha_composite(rb, image2)
    lb = Image.alpha_composite(i4, i3)
    lb = Image.alpha_composite(lb, image1)



    # modify brows
    angle = random() * t + t
    rb = rb.rotate(-angle,center=(634, 434))
    lb = lb.rotate(angle,center=(510, 434))

    if angle: x = int(9*4/angle)
    else: x = 0
    t9 = 1
    t8 = 0

    q = fr * 5 + fr * 10 * random()

    if q > 24: q = 24
    elif q < -19: q = -19

    x += q

    lb = lb.transform(lb.size, Image.AFFINE, (t9, t8, t8, t8, t9, x))
    rb = rb.transform(rb.size, Image.AFFINE, (t9, t8, t8, t8, t9, x))


    #choose eyes
    a = 2 + (random() * t)
    a = int(a)

    if a > 3: a = 3
    elif a < 1: a = 1

    it = i

    if( i==0 ):
        x = randint(0,1)
        if x == 1: it +=1
        else: it-=1

    if it > 0:
        a *= 2

    else:
        a = a*2-1

    i7 = Image.open('le' + str(a) + '.png')

    x = random()
    if x > 0.5:
        if a == 1: a = 2
        elif a == 2: a = 1
        elif a == 3: a = 6
        elif a == 4: a = 5
        elif a == 5: a = 4
        else: a == 3


    i8 = Image.open('re' + str(a) + '.png')
    i11 = Image.open('il.png')
    i12 = Image.open('ir.png')

    # choose pupils
    a = 3 + random()*ya
    a = int(a)

    i13 = Image.open('pl' + str(a) + '.png')
    i14 = Image.open('pr' + str(a) + '.png')
    le = Image.alpha_composite(i7, i11)
    le = Image.alpha_composite(le, i13)
    re = Image.alpha_composite(i8, i12)
    re = Image.alpha_composite(re, i14)

    # modify eyes
    x = 1 + ya/20 + (random() * ya / 35)

    if x < .85: x = .85

    n = int(1145*x)
    j = int(1138*x)
    le = le.resize((n,j))
    re = re.resize((n,j))

    t1 = int((1145-n)/2)
    t2 = int((1138-j)/2)

    q = 75*(x-1)

    lb = lb.transform(lb.size, Image.AFFINE, (t9, t8, t8, t8, t9, q))
    rb = rb.transform(rb.size, Image.AFFINE, (t9, t8, t8, t8, t9, q))

    lb.paste(le, (t1,t2), le.convert("RGBA"))
    rb.paste(re, (t1,t2), re.convert("RGBA"))

    l = lb
    r = rb

    # move eyes
    x = random()*i*8
    t9 = 1
    t8 = 0

    q = int((1 - (n / 1145)) * 105)

    l = l.transform(l.size, Image.AFFINE, (t9, t8, (x+q), t8, t9, t8))
    r = r.transform(r.size, Image.AFFINE, (t9, t8, (-x - q), t8, t9, t8))

    img = Image.alpha_composite(l, r)
    img = Image.alpha_composite(img, f)


    img.save('/Users/tobias/Desktop/SD/static/' + addr)

    count = count + 1

    t = t + 3
    fr = fr + 3
    i = i + 3
    ya = ya + 3

    return render_template('index.html', Trust = t, Friend = fr, Int = i, YA = ya, file = addr)


if __name__ == '__main__':
  app.run(debug=True)
