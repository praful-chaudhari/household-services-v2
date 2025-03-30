from flask import current_app as app, jsonify, send_from_directory, request
from .tasks import csv_report
from celery.result import AsyncResult
from flask_security import roles_required, auth_required
from datetime import datetime

cache = app.cache

@app.get('/test')
@cache.cached(timeout=30, key_prefix='test1')
def test():
    return jsonify({
        'message': 'Cache is working',
        'timestamp': datetime.now().isoformat()
    })

@app.get('/test/<int:id>')
@cache.cached(timeout=30, key_prefix= lambda: f'test2{request.path}')
def test2(id=None):
    return jsonify({
        'message': 'Cache is working',
        'timestamp': datetime.now().isoformat()
    })

@app.get('/delete')
def delete():
    cache_key = 'test1'
    
    # DELETE THE CACHE
    deleted = cache.delete(cache_key)
    
    return jsonify({
        'message': 'Cache deleted successfully' if deleted else 'Cache key not found',
        'cache_key_attempted': cache_key,
        'timestamp': datetime.now().isoformat()
    })

@app.get('/delete/<int:id>')
def delete2(id):
    cache_key = f'test2/test/{id}'
    deleted = cache.delete(cache_key)
    return jsonify({
        'message': 'Cache deleted successfully' if deleted else 'Cache key not found',
        'cache_key_attempted': cache_key,
        'timestamp': datetime.now().isoformat()
    })




@app.route('/api/export') # this manually triggers the job
@auth_required('token')
@roles_required('admin')
def export_csv():
    result = csv_report.delay() # async object
    return jsonify({
        'id': result.id,
        'result': result.result,
    })

@app.route('/api/csv_result/<task_id>') # this is used to check the status of the job or test the result
@auth_required('token')
@roles_required('admin')
def csv_result(task_id):
    res = AsyncResult(task_id)
    return send_from_directory('static', res.result)


