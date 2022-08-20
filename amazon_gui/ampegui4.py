import requests
import json
import time, smtplib, os, sys
from bs4 import BeautifulSoup
import tkinter
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

root = Tk(screenName=None,  baseName=None,  className='Amprer',  useTk=1)
image1 = Image.open("connect_database_frame01.png")
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test
label1.place(x=0, y=0)
root.title("Product Price Tracker")
x = tk.StringVar()
#header = Label(root, font='Helvetica 18 bold', pady=20)
#header.pack()
x =tk.StringVar()
flipkart = ''
olx = ''
amazon = ''

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}

def search():
    word =x.get()
    search = "https://www.google.com/search?q="+word
    #webbrowser.open_new(search)

def flipkart_fun():
    name = x.get()
    try:
        global flipkart
        name1 = name.replace(" ", "%20")
        flipkart = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(
            f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',
            headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip()  ### New Class For Product Name
        flipkart_name = flipkart_name.upper()
        if name.upper() in flipkart_name:
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()  ### New Class For Product Price
            msg1 = Label(root,font=( 'aria' ,16, ), text="Flipkart : ")
            msg1.place(x=500,y=300)
            price = Label(root,font=( 'aria' ,12, ), text=f"Price : {flipkart_price}")
            price.place(x=500,y=330)
        else:
            flipkart_price = '0'
        return flipkart_price
    except:
        flipkart_price = '0'
    return flipkart_price

def olx_fun():
    name = x.get()
    try:
        global olx
        name1 = name.replace(" ", "-")
        olx = f'https://www.olx.in/items/q-{name1}?isSearchCall=true'
        res = requests.get(f'https://www.olx.in/items/q-{name1}?isSearchCall=true', headers=headers)
        #print("\nSearching in OLX......")
        soup = BeautifulSoup(res.text, 'html.parser')
        olx_name = soup.select('._2tW1I')
        olx_page_length = len(olx_name)
        for i in range(0, olx_page_length):
            olx_name = soup.select('._2tW1I')[i].getText().strip()
            name = name.upper()
            olx_name = olx_name.upper()
            if name in olx_name:
                olx_price = soup.select('._89yzn')[i].getText().strip()
                olx_name = soup.select('._2tW1I')[i].getText().strip()
                olx_loc = soup.select('.tjgMj')[i].getText().strip()
                try:
                    label = soup.select('._2Vp0i span')[i].getText().strip()
                except:
                    label = "OLD"

                #print("Olx:")
                #print(label)
                #print(olx_name)
                #print(olx_price)
                #print(olx_loc)
                #print("-----------------------")
                break
            else:
                i += 1
                i = int(i)
                if i == olx_page_length:
                    print("Olx: No product Found!")
                    print("-----------------------")
                    olx_price = '0'
                    break
        msg1 = Label(root, font=('aria', 16,), text="Olx : ")
        msg1.place(x=500, y=360)
        price = Label(root, font=('aria', 12,), text=f"Price : {olx_price}")
        price.place(x=500, y=390)
        return olx_price
    except:
        print("Olx: No product found!")
        print("-----------------------")
        olx_price = '0'
    return olx_price

def amazon_fun():
    name = x.get()
    try:
        global amazon

        name1 = name.replace(" ", "%20")
        amazon = f'https://www.amazon.in/s?i=aps&k={name1}&ref=nb_sb_noss_2&url=search-alias%3Daps'
        res = requests.get(f'https://www.amazon.in/s?i=aps&k={name1}&ref=nb_sb_noss_2&url=search-alias%3Daps', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0, amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name[0:20]:
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                break
            else:
                i += 1
                i = int(i)
                if i == amazon_page_length:
                    amazon_price = '0'
                    break
        msg1 = Label(root, font=('aria', 16,), text="Amazon : ")
        msg1.place(x=500, y=420)
        price = Label(root, font=('aria', 12,), text=f"Price : {amazon_price}")
        price.place(x=500, y=450)
        return amazon_price
    except:
        amazon_price = '0'
    return amazon_price

def check_price():

    no_prod.pack_forget()
    trigger_Label.pack_forget()
    email = amazon_email1.get()
    title = x.get()
    tick_price = amazon_sel_price.get()


    flipkart_price = flipkart_fun()
    amazon_price = amazon_fun()
    olx_price = olx_fun()


    flipkart_price = convert(flipkart_price)
    amazon_price = convert(amazon_price)
    olx_price = convert(olx_price)

    lst = [flipkart_price, amazon_price, olx_price]
    # print(lst)
    lst2 = []
    for j in range(0, len(lst)):
        if lst[j] > 0:
            lst2.append(lst[j])
    if len(lst2) == 0:
        no_prod.pack()
    else:
        min_price = min(lst2)
        if int(tick_price) >= min_price:
            price = {
                f'{amazon_price}': f'{amazon}',
                f'{flipkart_price}': f'{flipkart}',
                f'{olx_price}': f'{olx}'
            }
            for key, value in price.items():
                if int(key) == min_price:
                    send_mail(email,value,key,title)
        else:
            no_prod.config(text = "Product not in range")
            no_prod.pack()

def convert(a):
    if a != '0':
        b=a.replace(" ",'')
        c=b.replace("INR",'')
        d=c.replace(",",'')
        f=d.replace("₹",'')
        e = f.replace("$", '')
        g=int(float(e))
        return g
    else :
        return int(a)

def send_mail(email,url,price,title):

    subject = title + 'is available at Rs.' + str(price) + '!'
    body = '\nCheck out the link: ' + url

    msg = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('your email id', 'your password')
        smtp.sendmail('your email id', email, msg)
        trigger_Label.pack()


#trigger_Label = Label(root, text='Email has been sent!', fg='green')
Product_Label = Label(root, text='Enter Product Name:', bg='white',font= ("Bahnschrift SemiBold", 11))
Product_Label.pack()
Product_Label.place(x=620, y=70)

b5 =tk.Button(root,text="Search",fg="white",bg="Dark Orange1",font= ("Bahnschrift SemiBold", 12), command=check_price)
b5.place(x=830,y=89,height=45,width=60)
e1 = tk.Entry(root,bg = "light pink",relief="ridge", borderwidth = 4,textvariable=x,font= ("Times New Roman", 12))
e1.place(x=520,y=95,width=300,height=35)

amazon_email_label1 = Label(root, text='Enter your email:', bg='white',font= ("Bahnschrift SemiBold", 11))
amazon_email_label1.pack()
amazon_email_label1.place(x=645, y=150)


global amazon_email1
amazon_email1 = Entry(root,relief="ridge", borderwidth = 4, width=30,font= ("Times New Roman", 12))
amazon_email1.pack()
amazon_email1.place(x=570, y=180)

global amazon_sel_price_label
amazon_sel_price_label = Label(root, text='Enter a trigger price for the email:', bg='white', font=("Bahnschrift SemiBold", 11))
amazon_sel_price_label.pack()
amazon_sel_price_label.place(x=585, y=220)
global amazon_sel_price
amazon_sel_price = (Entry(root,relief="ridge", borderwidth = 4, width=15,font= ("Times New Roman", 12)))
amazon_sel_price.pack()
amazon_sel_price.place(x=658, y=250,width= 100)

global trigger_Label
trigger_Label = Label(root, text='Email has been sent!', fg='green',font=("Bahnschrift SemiBold", 12))

global no_prod
no_prod = Label(root, text='Product Not Found', fg='red')



nochange_Label = Label(root)

scrollbar = Scrollbar(root)

global msg1
global price

root.wm_geometry("1366x768")
root.mainloop()