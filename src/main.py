import flet as ft
import sqlite3

def main(page: ft.Page):
    
    def register(e):
        db = sqlite3.connect('../it.progger.db')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login VARCHAR(100),                    
            pass VARCHAR(100)
        )""")

        sql = f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')"

        print(sql)

        cur.execute(sql)

        db.commit() 
        db.close()

        user_login.value = ''
        user_pass.value = ''
        page.update()

    def auth_user(e):
        db = sqlite3.connect('../it.progger.db')

        cur = db.cursor()

        cur.execute('SELECT * FROM users WHERE login = ? AND pass = ?', (user_login.value, user_pass.value))
        user = cur.fetchone()

        if user == None:
            page.snack_bar = ft.SnackBar(ft.Text('Неверный логин или пароль'))
            page.snack_bar.open = True
            page.update()
            return
        
        print(user)

        db.close()

        # user_login.value = ''
        # user_pass.value = ''
        # page.update()

    def validate(e):
        if (all([user_login.value, user_pass.value])): 
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        
        page.update()

    user_login = ft.TextField(label='Логин', width=200, on_change=validate)
    user_pass = ft.TextField(label='Пароль', width=200, on_change=validate, password=True)
    btn_reg = ft.OutlinedButton(text='Зарегистрироватся', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Войти', width=200, on_click=auth_user, disabled=True)

    panel_reg = ft.Row(
        [            
            ft.Column([
                ft.Text('Регистрация'),
                user_login,
                user_pass,
                btn_reg
            ])
        ], 
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    panel_auth = ft.Row(
        [            
            ft.Column([
                ft.Text('Авторизация'),
                user_login,
                user_pass,
                btn_auth
            ])
        ], 
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0:
            page.add(panel_reg)
        else:            
            page.add(panel_auth)
        
        page.update()
        print(page.navigation_bar.selected_index)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Регистрация'),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label='Авторизация')
        ],
        on_change=navigate
    )

    page.add(panel_reg)

ft.app(target=main)