from app_py.config.mysqlconnections import connectToMySQL

class Quote:
    def __init__(self, data):
        self.id_quote = data['id_quote']
        self.id_usuario = data['id_usuario']
        self.quote = data['quote']
        self.autor = data['autor']
    
    @classmethod
    def create_quote(cls,data):
        query = ('INSERT into quotes (id_usuario, quote, autor) VALUES (%(id_usuario)s,  %(quote)s, %(autor)s)')
        return connectToMySQL('exam2_python').query_db(query,data)
    
    
    @classmethod
    def get_all(cls):
        query = (
            'SELECT quotes.quote, quotes.autor, usuario.first_name, usuario.last_name '
            'FROM quotes '
            'LEFT JOIN usuario ON usuario.id_usuario = quotes.id_usuario'
        )
        resultados = connectToMySQL('exam2_python').query_db(query)
        if resultados:
            quotes = [(row['quote'], row['autor'], row['first_name'], row['last_name']) for row in resultados]
            return quotes
        else: 
            return None