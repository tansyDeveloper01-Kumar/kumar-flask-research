from flask import Flask, request, jsonify
import pymysql

connection = pymysql.connect(host='104.199.137.128',
                             user='masterdbuser',
                             password='xx9mastermysql6xx',
                             db='sama_master',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login(self):
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
                                     data[0]['sql_user_id'],
                                     data[0]['sql_password'],
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
                        self.login.commit()
                        # login.execute("SELECT @oparam_audit_screen_visit, @oparam_user_id")
                        # Fetch all the rows in a list of lists.
                        results = [login.fetchall()]
                        while login.nextset():
                            results.append(login._nextset(True))
                        print(results)                           
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


@app.route('/pro-delete', methods=['DELETE'])
def inv_prd_del():
    try:
        with connection.cursor() as conn:
            try:
                datas = request.get_json()
                user_id = datas.get('user_id')
                entity_id = datas.get('entity_id')
                login_name = user_id.split('@', 1)[0]
                password = datas.get('password')
                domain_name = user_id.split('@', 1)[1]
                args = [domain_name, 1, 1, 0, 0, 0]
                conn.callproc('sproc_sama_get_client_db_connnection_info_v2', args)                
                data = conn.fetchall()
                
                db = pymysql.connect("104.199.137.128",
                                     "salman",
                                     "1salman3",
                                     "dev_tss_demo02",
                                    )                
                token = data[0]['v_token']
                database_name = "dev_tss_demo02"
                
                try:                    
                    args = [token, 0, 0, 0]
                    conn.callproc('sproc_sama_validate_token', args)
                    verify_token_data = conn.fetchall()
                    if token == verify_token_data[0].get('token'):
                        login = db.cursor()
                        output_params = [0, 0, 0]
                        args = [int(entity_id), 1767, 20, 110001, 1, 1, *output_params]
                        try:
                            login.callproc("sproc_inv_product_dml_del",args)
                            return jsonify({
                                'message': 'Product deleted successfully'
                            }), 200
                        except Exception as e:
                            return jsonify({
                                'message': e
                            }), 400
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


@app.route('/pro-grid', methods=['GET'])
def inv_prd_grid():
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
                
                db = pymysql.connect("104.199.137.128",
                                     "salman",
                                     "1salman3",
                                     "dev_tss_demo02",
                                    )                
                token = data[0]['v_token']
                database_name = "dev_tss_demo02"
                
                try:                    
                    args = [token, 0, 0, 0]
                    conn.callproc('sproc_sama_validate_token', args)
                    verify_token_data = conn.fetchall()
                    if token == verify_token_data[0].get('token'):
                        login = db.cursor()
                        output_params = [0, 0, 0]
                        args = [1767, 20, 110001, 1, 1, *output_params]
                        
                        login.callproc("sproc_inv_product_grid",args)
                        results = [login.fetchall()]
                        # login.execute("SELECT @oparam_audit_screen_visit, @oparam_user_id")
                        # Fetch all the rows in a list of lists.
                        # results = [login.fetchall()]
                        # while login.nextset():
                        #     results.append(login.callproc("SELECT @oparam_audit_screen_visit , @oparam_session_id"))
                        # print(results)                           
                        return jsonify({
                            'message': 'Product grid fetched successfully',
                            'results': results
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




if __name__ == '__main__':
    app.run(port=5000, debug=True)