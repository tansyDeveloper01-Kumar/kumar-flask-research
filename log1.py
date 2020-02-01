from flask import Flask, request, jsonify
import pymysql

# db_driver = 'mysql+pymysql'
# db_host = '104.199.137.128'
# db_user = 'devmysql'
# db_pass = 'abcdevmysqlxx'
# db_name = 'dev_tss_demo02'

# db = pymysql.connect(
#             db_host,
#             db_user,
#             db_pass,
#             db_name)

connection = pymysql.connect(host='104.199.137.128',
                             user='masterdbuser',
                             password='xx9mastermysql6xx',
                             db='sama_master',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        with connection.cursor() as conn:
            try:
                datas = request.get_json()
                user_id = datas.get('user_id')
                login_name = user_id.split('@', 1)[0]
                password = datas.get('password')
                domain_name = user_id.split('@', 1)[1]
                args = [domain_name, 1, 1, 0, 0, 0]
                conn.callproc('sproc_sama_get_client_db_connnection_info_v2', args)                
                data = conn.fetchall()
                
                db = pymysql.connect(data[0]['db_server'],
                                     "devmysql",
                                     "abcdevmysqlxx",
                                     data[0]['database_name'],
                                    )                
                token = data[0]['v_token']
                database_name = data[0]['database_name']
                try:                    
                    args = [token, 0, 0, 0]
                    conn.callproc('sproc_sama_validate_token', args)
                    verify_token_data = conn.fetchall()
                    if token == verify_token_data[0].get('token'):
                        login = db.cursor()
                        sql = "sproc_sec_login_v2"
                        output_params = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                        args = [login_name, password, '10.2.3.4', 'desktop', *output_params]
                        login.callproc(sql,args)
                        # login.execute("SELECT @oparam_audit_screen_visit, @oparam_user_id")
                        # Fetch all the rows in a list of lists.
                        results = [login.fetchall()]
                        # while login.nextset():
                        #     results.append(login.callproc("SELECT @oparam_audit_screen_visit , @oparam_session_id"))
                        # print(results)                           
                        return jsonify({
                            'message': 'Login data',
                            'data': results
                        }), 200
                    else:
                        return jsonify({
                            'message': 'Token verification failed'
                        }), 400
                except Exception as error:
                    error_response = str(error)
                    return jsonify({
                        'message': 'Fetching errors',
                        'data': error_response
                    }), 400
                finally:
                    conn.close()
                
            except Exception as error:
                response = str(error)
                return response
            finally:
                conn.close()
    except Exception as error:
        response = str(error)
        return response

@app.route('/brand', methods=['GET'])
def lkp_inv_brand():
    try:
        with db.cursor() as conn:
            try:
                args = [1767, 20, 110001, 1, 1, 0, 0, 0]
                conn.callproc('sproc_inv_lkp_brand', args)
                data = conn.fetchall()
                return jsonify({
                    'message': 'Fetching brand details',
                    'data': data
                }), 200
            except Exception as error:
                response = str(error)
                return response
            finally:
                conn.close()
    except Exception as error:
        response = str(error)
        return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)