from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria para los libros
books = []

@app.route('/api/v1/books', methods=['GET'])
def get_books():
    sort_by = request.args.get('sort_by')
    include_isbn = request.args.get('include') == 'isbn'
    
    lista = list(books)
    if sort_by == 'author':
        lista = sorted(lista, key=lambda x: str(x.get('author', '')).lower())
        
    return jsonify(lista), 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b.get('id') == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({'error': 'Libro no encontrado'}), 404

@app.route('/api/v1/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400
    books.append(data)
    return jsonify(data), 201

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    for b in books:
        if b.get('id') == book_id:
            b.update(data)
            return jsonify(b), 200
    return jsonify({'error': 'Libro no encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)