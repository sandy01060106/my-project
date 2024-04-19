#建立mongo資料庫連線
import pymongo
client=pymongo.MongoClient('mongodb+srv://haha:haha@cluster1.peavewk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
db=client.member_system#選擇操作 member_system 資料庫
print('資料庫建立成功')
#建立FLASK伺服器
from flask import *
app=Flask(
    __name__,
    static_folder='static',#自訂靜態檔案的資料夾名稱
    static_url_path='/'#自訂靜態檔案的對應網址路徑
    )
#建立application 物件(物件是指把盒子變成另一種屬性)，可以設定靜態檔案的網路處理
#所有建立在static資料夾下的檔案，都對應到網址路徑/static/檔案名稱
app.secret_key='any string but secret'#設定session的密鑰，讓後端記得前端資料

#建立網站的回應方式，建立路徑 / 對應的處理函式
@app.route('/')
def home(): #用來回應網站首頁連線的函式，用來回應路徑 / 的處理函式
    return render_template('home.html') #回傳網站首頁的內容

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/database',methods=['POST'])
def database():
    #從前端接收資料
    nickname=request.form['nickname']
    email=request.form['email']
    password=request.form['password']
    #將接收到的資料與資料庫互動
    collection=db.users
    result=collection.find_one({
        'email':email
    })
    if result !=None:
        return redirect('/error?msg=信箱已被註冊')
    else:
        collection.insert_one({
            'nickname': nickname,
            'email': email,
            'password': password
        })
        return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    # 從前端接收資料
    email = request.form['email']
    password = request.form['password']
    # 將接收到的資料與資料庫互動
    collection = db.users
    #檢查信箱與密碼是否正確
    member=collection.find_one({
        '$and':[
            {'email': email},
            {'password': password}
        ]
    })
    if member!=None:#登入成功，在session紀錄會員資訊，導向到會員頁面
        session['nickname']=member['nickname']
        return redirect('/member')
    else:#找不到對應資料，登入失敗，導向到錯誤頁面
        return redirect('/error?msg=信箱或密碼輸入錯誤')

@app.route('/member')
def member():#確保會員是從登入頁面進入會員頁面，所以用session紀錄會員資料
    if 'nickname' in session:
        return render_template('member.html',nickname=session['nickname'])
    else:#若有人直接輸入會員網址會被導向到首頁
        return redirect('/')

@app.route('/logout')
def logout():#移除session裡的會員資料
    del session['nickname']
    return redirect('/')
@app.route('/error')
def error():
    message=request.args.get('msg','發生錯誤，請聯絡客服')
    return render_template('error.html',errorMsg=message)

app.run(port=3000)#啟動網站伺服器，可透過port參數指定埠號

