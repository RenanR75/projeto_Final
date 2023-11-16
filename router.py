from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import connection

router = APIRouter()
templates = Jinja2Templates(directory="templates")


    #ate aqui...
    # Adicionando a rota para mostrar o formulário de atualização
@router.get("/updateCurso/{idcurso}", response_class=HTMLResponse)    
def show_update_curso_form(request: Request, idcurso: int):
    mycursor = connection.mydb.cursor(dictionary=True)

    # Consulta SQL para obter os detalhes do curso com base no ID
    sql = "SELECT * FROM cursos WHERE idcurso = %s"
    mycursor.execute(sql, (idcurso,))
    curso = mycursor.fetchone()

    mycursor.close()

    # Adicione 'return' antes da chamada para TemplateResponse
    return templates.TemplateResponse("update_curso_form.html", {"request": request, "curso": curso})

def update_curso(idcurso: int, nome: str, descricao: str, carga: int, totaulas: int, ano: int):
    mycursor = connection.mydb.cursor()

    try:
        # Executa a atualização do curso no banco de dados
        sql = "UPDATE cursos SET nome = %s, descricao = %s, carga = %s, totaulas = %s, ano = %s WHERE idcurso = %s"
        values = (nome, descricao, carga, totaulas, ano, idcurso)
        mycursor.execute(sql, values)
        connection.mydb.commit()
        return True  # Retorna True se a atualização for bem-sucedida
    except Exception as e:
        # Lida com erros durante a atualização
        print(f"Erro durante a atualização do curso: {e}")
        return False  # Retorna False se a atualização falhar
    finally:
        mycursor.close()

# Suas rotas existentes abaixo
@router.post("/updateCurso/{idcurso}", response_class=HTMLResponse)
def update_curso_form(
    request: Request,
    idcurso: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    carga: int = Form(...),
    totaulas: int = Form(...),
    ano: int = Form(...),
):
    if update_curso(idcurso, nome, descricao, carga, totaulas, ano):
        return templates.TemplateResponse("update_curso_success.html", {"request": request, "idcurso": idcurso})
    else:
        # Lógica para lidar com falha na atualização
        return templates.TemplateResponse("update_curso_fail.html", {"request": request, "idcurso": idcurso})

    





# Adicionando a função para deletar o curso do banco de dados
def delete_curso(idcurso: int):
    mycursor = connection.mydb.cursor()

    # Consulta SQL para deletar o curso
    sql = "DELETE FROM cursos WHERE idcurso = %s"
    val = (idcurso,)

    mycursor.execute(sql, val)
    connection.mydb.commit()

    mycursor.close()

# Adicionando a rota para mostrar o formulário de exclusão
@router.get("/deleteCurso/{idcurso}", response_class=HTMLResponse)
def show_delete_curso_form(request: Request, idcurso: int):
    return templates.TemplateResponse("delete_curso_form.html", {"request": request, "idcurso": idcurso})

# Adicionando a rota para processar a exclusão do curso
@router.post("/deleteCurso")
def delete_curso_form(request: Request, idcurso: int = Form(...)):
    delete_curso(idcurso)
    return templates.TemplateResponse("delete_curso_sucess.html", {"request": request, "idcurso": idcurso})

# Restante do seu código existente
@router.get("/getCursos", response_class=HTMLResponse)
def get_cursos(request: Request):
    cursos_list = []
    mycursor = connection.mydb.cursor(dictionary=True)

    # Consulta SQL para obter todos os cursos
    sql = "SELECT * FROM cursos"
    mycursor.execute(sql)

    for data_cursos in mycursor:
        cursos_list.append(data_cursos)

    mycursor.close()
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos_list})
