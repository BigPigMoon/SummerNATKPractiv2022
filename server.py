import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import mysql.connector
import logging
import json


def unicode2str(ch: str) -> str:
    return bytes([int('0x'+i, base=16) for i in ch.split('%')[1:]]).decode('utf-8')


class Server(BaseHTTPRequestHandler):

    """ --------- mey be it will be need ¯\_(ツ)_/¯ ----------------
    def do_GET(self):
        db = mysql.connector.connect(
            host='localhost', user='root', 
            password='', database='kino')

        cursor = db.cursor()

        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))

        table = query_components['table']
        field = query_components['field']
        ch = query_components['char']
        
        ch = unicode2str(ch)

        sql = f"select * from {table} where {field} like '%{ch}%'"
        
        cursor.execute(sql)
        result = cursor.fetchall()

        data = {'data': []}

        for i in result:
            data['data'].append({
                'id': i[0],
                'name': i[1],
                })
            
            if type(i[2]) is datetime.date:
                data['data'][-1]['other'] = str(i[2])
            else:
                data['data'][-1]['other'] = i[2]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(data).encode('utf-8'))
    """

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        components = dict(qc.split("=") for qc in body.decode('utf-8').split("&"))
        components['char'] = unicode2str(components['char'])

        data = self.do_data(components)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_data(self, comps):
        db = mysql.connector.connect(
            host='localhost', user='root', 
            password='', database='kino')
        cursor = db.cursor()

        data = {'data': []}

        if comps['comma'] == 'select':
            self.select(cursor, comps, data)
        elif comps['comma'] == 'update':
            self.update()
        elif comps['comma'] == 'delete':
            self.delte()
        elif comps['comma'] == 'insert':
            self.insert()
            
        return data
    
    def select(self, cursor, comps, data):
        sql = f"""select * from {comps['table']}
        where {comps['field']} like '%{comps['char']}%'"""

        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            data['data'].append({'id': i[0], 'name': i[1],})
            
            if type(i[2]) is datetime.date:
                data['data'][-1]['other'] = str(i[2])
            else:
                data['data'][-1]['other'] = i[2]

    def insert(self, cursor, comps):
        pass

    def update(self):
        pass
    
    def delete(self):
        pass



def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd... \n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    logging.info('Stopping httpd...\n')


run()
