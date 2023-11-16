from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import connection
from router import router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Página inicial
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Adicione outras rotas, se necessário
app.include_router(router)

# Adicione esta rota abaixo das outras rotas


# Rota para obter todos os cursos
@app.get("/getCursos", response_class=HTMLResponse)
def get_cursos(request: Request):
    cursos_list = []
    mycursor = connection.mydb.cursor(dictionary=True)
    sql = "SELECT * FROM cursos"
    mycursor.execute(sql)
    for data_cursos in mycursor:
        cursos_list.append(data_cursos)
    mycursor.close()
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos_list})

# Rota para mostrar o formulário de adição de cursos
@app.get("/addCurso", response_class=HTMLResponse)
def show_add_curso_form(request: Request):
    return templates.TemplateResponse("add_curso_form.html", {"request": request})

# Rota para processar o envio do formulário e adicionar um novo curso
@app.post("/addCurso", response_class=HTMLResponse)
def add_curso(
    request: Request,
    idcurso: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    carga: int = Form(...),
    totaulas: int = Form(...),
    ano: int = Form(...),
    
    
):
    mycursor = connection.mydb.cursor(dictionary=True)

    # Verifica se o ID especificado já existe na tabela
    mycursor.execute("SELECT idcurso FROM cursos WHERE idcurso = %s", (idcurso,))
    existing_id = mycursor.fetchone()

    if existing_id:
        # Se o ID já existe, encontre o próximo ID disponível
        mycursor.execute("SELECT MAX(idcurso) FROM cursos")
        max_id = mycursor.fetchone()["MAX(idcurso)"]
        idcurso = max_id + 1

    # Insere o novo curso no banco de dados
    sql = "INSERT INTO cursos (idcurso, nome, descricao, carga, totaulas, ano) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (idcurso, nome, descricao, carga, totaulas, ano)
    mycursor.execute(sql, values)
    mycursor.execute("COMMIT;")
    mycursor.close()

    return templates.TemplateResponse("add_curso_success.html", {"request": request, "nome": nome})
app.include_router(router)
