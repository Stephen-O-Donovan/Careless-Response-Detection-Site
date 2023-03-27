import json

from flask import request
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict


from app.api import blueprint
from app.authentication.decorators import token_required

from app.api.forms import *
from app.models    import *

api = Api(blueprint)


@api.route('/survey/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/survey/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class SurveyRoute(Resource):
    def get(self, model_id: int = None):
        if model_id is None:
            all_objects = Survey.query.all()
            output = [{'id': obj.id, **SurveyForm(obj=obj).data} for obj in all_objects]
        else:
            obj = Survey.query.get(model_id)
            if obj is None:
                return {
                           'message': 'matching record not found',
                           'success': False
                       }, 404
            output = {'id': obj.id, **SurveyForm(obj=obj).data}
        return {
                   'data': output,
                   'success': True
               }, 200

    @token_required
    def post(self):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}
        form = SurveyForm(MultiDict(body_of_req))
        if form.validate():
            try:
                obj = Survey(**body_of_req)
                Survey.query.session.add(obj)
                Survey.query.session.commit()
            except Exception as e:
                return {
                           'message': str(e),
                           'success': False
                       }, 400
        else:
            return {
                       'message': form.errors,
                       'success': False
                   }, 400
        return {
                   'message': 'record saved!',
                   'success': True
               }, 200

    @token_required
    def put(self, model_id: int):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}

        to_edit_row = Survey.query.filter_by(id=model_id)

        if not to_edit_row:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        obj = to_edit_row.first()

        if not obj:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        form = SurveyForm(MultiDict(body_of_req), obj=obj)
        if not form.validate():
            return {
                       'message': form.errors,
                       'success': False
                   }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__['_raw_columns'][0].columns._all_columns]

        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(obj, col, value)
        Survey.query.session.add(obj)
        Survey.query.session.commit()
        return {
            'message': 'record updated',
            'success': True
        }

    @token_required
    def delete(self, model_id: int):
        to_delete = Survey.query.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404
        to_delete.delete()
        Survey.query.session.commit()
        return {
                   'message': 'record deleted!',
                   'success': True
               }, 200


@api.route('/tests/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/tests/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class TestRoute(Resource):
    def get(self, model_id: int = None):
        if model_id is None:
            all_objects = Test.query.all()
            output = [{'id': obj.id, **TestForm(obj=obj).data} for obj in all_objects]
        else:
            obj = Test.query.get(model_id)
            if obj is None:
                return {
                           'message': 'matching record not found',
                           'success': False
                       }, 404
            output = {'id': obj.id, **TestForm(obj=obj).data}
        return {
                   'data': output,
                   'success': True
               }, 200

    @token_required
    def post(self):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}
        form = TestForm(MultiDict(body_of_req))
        if form.validate():
            try:
                obj = Test(**body_of_req)
                Test.query.session.add(obj)
                Test.query.session.commit()
            except Exception as e:
                return {
                           'message': str(e),
                           'success': False
                       }, 400
        else:
            return {
                       'message': form.errors,
                       'success': False
                   }, 400
        return {
                   'message': 'record saved!',
                   'success': True
               }, 200

    @token_required
    def put(self, model_id: int):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}

        to_edit_row = Test.query.filter_by(id=model_id)

        if not to_edit_row:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        obj = to_edit_row.first()

        if not obj:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        form = TestForm(MultiDict(body_of_req), obj=obj)
        if not form.validate():
            return {
                       'message': form.errors,
                       'success': False
                   }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__['_raw_columns'][0].columns._all_columns]

        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(obj, col, value)
        Test.query.session.add(obj)
        Test.query.session.commit()
        return {
            'message': 'record updated',
            'success': True
        }

    @token_required
    def delete(self, model_id: int):
        to_delete = Test.query.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404
        to_delete.delete()
        Test.query.session.commit()
        return {
                   'message': 'record deleted!',
                   'success': True
               }, 200

