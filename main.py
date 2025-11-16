from flask import Flask, request, make_response, jsonify
import mysql.connector

db=mysql.connector.connect(
    host='localhost',
    user='root',
    password='MysqlDatabase1',
    database='projeto'
)

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/carros', methods=['GET'])
def get_carros():
    cursor=db.cursor()
    sql='SELECT * FROM carros'
    cursor.execute(sql)
    meus_carros=cursor.fetchall()
    carros=list()

    for carro in meus_carros:
        carros.append(
            {
                'id': carro[0],
                'marca': carro[1],
                'modelo': carro[2],
                'ano': carro[3]
            }
            
        )
    return make_response(jsonify(
            mensagem='Lista de carros.',
            carros=carros
        )
    )

@app.route('/carros', methods=['POST'])
def create_carro():
    carro = request.json
    
    sql = 'INSERT INTO carros (marca, modelo, ano) VALUES (%s, %s, %s)'
    valores = (carro['marca'], carro['modelo'], carro['ano'])
    cursor = db.cursor()
    cursor.execute(sql, valores)
    db.commit()

    return make_response(jsonify(
            mensagem='Carro cadastrado com sucesso.',
            carro=carro
        )
    )

app.run()