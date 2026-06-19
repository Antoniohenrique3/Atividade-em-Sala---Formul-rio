from flask import Flask, request, jsonify, render_template, redirect, url_for
import dados



biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template ('index.html')

@app.route('/biblioteca')
def biblio():
    return render_template ('biblioteca.html', meuhtml=biblioteca, meunome='Antonio')

@app.route('/biblioteca', methods=['GET', 'POST'])
def interface_web():
    biblioteca = dados.carregar_do_arquivo()

    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'deletar':
            isbn = request.form.get('isbn')
            for l in biblioteca:
                if l["isbn"] == isbn:
                    biblioteca.remove(l)
                    dados.salvar_no_arquivo(biblioteca)
            return render_template('biblioteca.html', meuhtml=biblioteca)
    biblioteca = dados.carregar_do_arquivo()
    return render_template('biblioteca.html', meuhtml=biblioteca)

@app.route('/api/biblioteca', methods=['GET', 'POST'])
@app.route('/api/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def func_biblioteca(isbn=None):
    if request.method == 'GET':
        if isbn:
         if isbn == l['isbn']:
            resultados = [l for l in biblioteca if isbn == l['isbn']]
            if resultados:
                return resultados
            else:
                return "Nenhum livro encontrado"
        else:
            return jsonify(biblioteca)

    elif request.method == 'POST':
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return "Livro salvo", 201

    elif request.method == 'DELETE':
        for l in biblioteca:
                biblioteca.remove(l)
                dados.salvar_no_arquivo(biblioteca)
                return "livro apagado"
        else:
            return "Nenhum livro encontrado"

    elif request.method == 'PUT':
        alteracoes = request.get_json()

        for livro in biblioteca:
            if isbn == livro['isbn']:
                print(livro['isbn'])
                for key, value in alteracoes.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return 'dado alterado com sucesso', 220
        return "Solicitação Inválida", 404
    else:
        return 404

@app.route('/biblioteca/criar', methods=['GET', 'POST'])
def cria_livro():
    if request.method == 'POST':
        novo_livro = {
            "isbn" : request.form.get("isbn"),
            "titulo" : request.form.get("titulo"),
            "autor"  : request.form.get("autor"),
            "genero" : request.form.get("genero"),
            "ano_publicacao" : request.form.get("ano_publicacao"),
            "editora" : request.form.get("editora"),
            "paginas" : request.form.get("paginas"),
            "status" : request.form.get("status"),
            "localizacao" : request.form.get("localizacao")
        }

        for l in biblioteca:
                if l['isbn'] == novo_livro['isbn']:
                    return jsonify("Livro já está cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return redirect(url_for('interface_web'))
    else:
        return render_template('criar_livro.html')

@app.route('/biblioteca/alterar', methods=['GET', 'POST'])
def altera_livro():
    print(request.args.get('isbn'))
    if request.method == 'POST':
        alterado_livro = {
            "isbn" : request.form.get("isbn"),
            "titulo" : request.form.get("titulo"),
            "autor"  : request.form.get("autor"),
            "genero" : request.form.get("genero"),
            "ano_publicacao" : request.form.get("ano_publicacao"),
            "editora" : request.form.get("editora"),
            "paginas" : request.form.get("paginas"),
            "status" : request.form.get("status"),
            "localizacao" : request.form.get("localizacao")
        }

        for l in biblioteca:
                if l['isbn'] == alterado_livro['isbn']:
                     l.update(alterado_livro)
                     dados.salvar_no_arquivo(biblioteca)
        return redirect(url_for('interface_web'))
    else:
        for l in biblioteca:
            if l['isbn'] == request.args.get('isbn'):
                return render_template('alterar_livro.html', livro = l)

if __name__ == "__main__":
    app.run(debug=True)