from flask import Flask, render_template, redirect, url_for, flash, request    
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user    
    
app = Flask(__name__)    
app.secret_key = 'your_very_secret_key'  # 请替换为一个更安全的密钥    
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 增加安全性    
app.config['REMEMBER_COOKIE_HTTPONLY'] = True  # 增加安全性    
    
login_manager = LoginManager(app)    
login_manager.login_view = 'login'    
login_manager.session_protection = 'strong'  # 增加会话保护    
    
# 假设的用户数据（实际应存储在数据库中并使用哈希密码）    
users_data = {    
    'admin': {'password': 'hashed_admin_password'}  # 请使用哈希函数生成哈希密码    
}    
    
class User(UserMixin):    
    def __init__(self, username):    
        self.username = username    
    
    def check_password(self, password):    
        # 在实际中，这里应该使用哈希验证函数    
        return users_data.get(self.username, {}).get('password') == password    
    
    def get_id(self):  # 重写 get_id 方法  
        return self.username  # 返回用户名作为唯一标识符  
    
    @staticmethod    
    def get(username):    
        return User(username) if username in users_data else None    
    
@login_manager.user_loader    
def load_user(user_id):    
    # 注意：这里 user_id 应该是用户名，因为我们没有使用数据库 ID    
    return User.get(user_id)    
    
@app.route('/')    
def login():    
    if current_user.is_authenticated:    
        return redirect(url_for('about'))    
    return render_template('login.html')    
    
@app.route('/login', methods=['POST'])    
def login_post():    
    username = request.form['username']    
    password = request.form['password']    
    user = User.get(username)    
    if user and user.check_password(password):    
        login_user(user, remember=request.form.get('remember'))    
        flash('You were logged in successfully!', 'success')    
        return redirect(url_for('about'))    
    flash('Invalid username or password', 'danger')    
    return redirect(url_for('login'))    
    
@app.route('/about')    
@login_required    
def about():    
    return render_template('about.html')    
    
@app.route('/logout')    
@login_required    
def logout():    
    logout_user()    
    flash('You were logged out successfully!', 'info')    
    return redirect(url_for('login'))    
    
if __name__ == '__main__':    
    app.run(debug=True)