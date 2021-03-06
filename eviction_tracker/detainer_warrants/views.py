import operator
from flask import Blueprint
from flask_security import current_user, AnonymousUser
from flask_resty import (
    ApiError,
    AuthorizeModifyMixin,
    HasAnyCredentialsAuthorization,
    HasCredentialsAuthorizationBase,
    HeaderAuthenticationBase,
    ColumnFilter,
    GenericModelView,
    CursorPaginationBase,
    RelayCursorPagination,
    Filtering,
    Sorting,
    meta,
    model_filter
)

from sqlalchemy import and_, or_
from sqlalchemy.orm import raiseload

from eviction_tracker.database import db
from .models import DetainerWarrant, Attorney, Defendant, Courtroom, Plaintiff, Judge, Judgement, PhoneNumberVerification
from .serializers import *
from eviction_tracker.permissions.api import HeaderUserAuthentication, Protected, OnlyMe, CursorPagination, AllowDefendant


@model_filter(fields.String())
def filter_name(model, name):
    return model.name.ilike(f'%{name}%')


@model_filter(fields.String())
def filter_first_name(model, name):
    return model.first_name.ilike(f'%{name}%')


@model_filter(fields.String())
def filter_last_name(model, name):
    return model.last_name.ilike(f'%{name}%')


class AttorneyResourceBase(GenericModelView):
    model = Attorney
    schema = attorney_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('id', default='-id')
    filtering = Filtering(
        name=filter_name,
    )


class AttorneyListResource(AttorneyResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class AttorneyResource(AttorneyResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)


class DefendantResourceBase(GenericModelView):
    model = Defendant
    schema = defendant_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('id', default='-id')
    filtering = Filtering(
        first_name=filter_first_name,
        last_name=filter_last_name
    )


class DefendantListResource(DefendantResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class DefendantResource(DefendantResourceBase):
    def get(self):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)


class CourtroomResourceBase(GenericModelView):
    model = Courtroom
    schema = courtroom_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('id', default='-id')
    filtering = Filtering(
        name=filter_name,
    )


class CourtroomListResource(CourtroomResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class CourtroomResource(CourtroomResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)


class PlaintiffResourceBase(GenericModelView):
    model = Plaintiff
    schema = plaintiff_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('id', default='-id')
    filtering = Filtering(
        name=filter_name,
    )


class PlaintiffListResource(PlaintiffResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class PlaintiffResource(PlaintiffResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)


class JudgeResourceBase(GenericModelView):
    model = Judge
    schema = judge_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('id', default='-id')
    filtering = Filtering(
        name=filter_name,
    )


class JudgeListResource(JudgeResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class JudgeResource(JudgeResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)


class JudgementResourceBase(GenericModelView):
    model = Judgement
    schema = judgement_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('court_date', default='-court_date')


class JudgementListResource(JudgementResourceBase):
    def get(self):
        return self.list()

    def post(self):
        return self.create()


class JudgementResource(JudgementResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.update(int(id), partial=True)

    def delete(self, id):
        return self.destroy(int(id))


@model_filter(fields.String())
def filter_defendant_name(model, defendant_name):
    return model._defendants.any(Defendant.first_name.ilike(f'%{defendant_name}%'))


@model_filter(fields.String())
def filter_address(model, address):
    return model._defendants.any(Defendant.address.ilike(f'%{address}%'))


@model_filter(fields.String())
def filter_plaintiff_name(model, plaintiff_name):
    return model._plaintiff.has(Plaintiff.name.ilike(f'%{plaintiff_name}%'))


@model_filter(fields.String())
def filter_plaintiff_attorney_name(model, plaintiff_attorney_name):
    return model._plaintiff_attorney.has(Attorney.name.ilike(f'%{plaintiff_attorney_name}%'))


class DetainerWarrantResourceBase(GenericModelView):
    model = DetainerWarrant
    schema = detainer_warrant_schema
    id_fields = ('docket_id',)

    authentication = HeaderUserAuthentication()
    authorization = AllowDefendant()

    pagination = CursorPagination()
    sorting = Sorting('file_date', default='-file_date')
    filtering = Filtering(
        docket_id=ColumnFilter(operator.eq),
        defendant_name=filter_defendant_name,
        file_date=ColumnFilter(operator.eq),
        plaintiff=filter_plaintiff_name,
        plaintiff_attorney=filter_plaintiff_attorney_name,
        address=filter_address
    )


class DetainerWarrantListResource(DetainerWarrantResourceBase):
    def get(self):
        return self.list()


class DetainerWarrantResource(DetainerWarrantResourceBase):
    def get(self, id):
        return self.retrieve(id)

    def patch(self, id):
        return self.upsert(id)


class PhoneNumberVerificationResourceBase(GenericModelView):
    model = PhoneNumberVerification
    schema = phone_number_verification_schema

    authentication = HeaderUserAuthentication()
    authorization = Protected()

    pagination = CursorPagination()
    sorting = Sorting('phone_number', default='phone_number')


class PhoneNumberVerificationListResource(PhoneNumberVerificationResourceBase):
    def get(self):
        return self.list()


class PhoneNumberVerificationResource(PhoneNumberVerificationResourceBase):
    def get(self, id):
        return self.retrieve(id)
