from marshmallow import Schema, fields


class DistrictSchema(Schema):
    class Meta:
        fields = ("id", "name")


district_schema = DistrictSchema()
districts_schema = DistrictSchema(many=True)


class AttorneySchema(Schema):
    class Meta:
        fields = ("id", "name", "district_id")


attorney_schema = AttorneySchema()
attorneys_schema = AttorneySchema(many=True)


class PhoneNumberVerificationSchema(Schema):
    class Meta:
        fields = ("caller_name", "caller_type", "phone_type",  "error_code", "carrier",
                  "country_code", "national_format", "phone_number")


phone_number_verification_schema = PhoneNumberVerificationSchema()
phone_number_verifications_schema = PhoneNumberVerificationSchema(many=True)


class DefendantSchema(Schema):
    verified_phone = fields.Nested(
        PhoneNumberVerificationSchema)

    class Meta:
        fields = ("id", "name", "first_name", "middle_name", "last_name", "suffix", "address",
                  "verified_phone", "potential_phones", "district_id")


defendant_schema = DefendantSchema()
defendants_schema = DefendantSchema(many=True)


class CourtroomSchema(Schema):
    class Meta:
        fields = ("id", "name", "district_id")


courtroom_schema = CourtroomSchema()
courtrooms_schema = CourtroomSchema(many=True)


class PlaintiffSchema(Schema):
    class Meta:
        fields = ("id", "name", "district_id")


plaintiff_schema = PlaintiffSchema()
plaintiffs_schema = PlaintiffSchema(many=True)


class JudgeSchema(Schema):
    class Meta:
        fields = ("id", "name", "district_id")


judge_schema = JudgeSchema()
judges_schema = JudgeSchema(many=True)


class DetainerWarrantSchema(Schema):
    plaintiff = fields.Nested(PlaintiffSchema)
    plaintiff_attorney = fields.Nested(AttorneySchema)
    courtroom = fields.Nested(CourtroomSchema)
    presiding_judge = fields.Nested(JudgeSchema)
    defendants = fields.Nested(DefendantSchema, many=True)

    amount_claimed = fields.Float(allow_none=True)
    court_date = fields.Date(allow_none=True)
    is_cares = fields.Bool(allow_none=True)
    is_legacy = fields.Bool(allow_none=True)
    nonpayment = fields.Bool(allow_none=True)
    notes = fields.String(allow_none=True)

    class Meta:
        fields = ("docket_id", "file_date", "status", "court_date", "amount_claimed", "amount_claimed_category",
                  "judgement", "judgement_notes", "plaintiff", "plaintiff_attorney", "courtroom", "presiding_judge", "defendants",
                  "zip_code", "is_legacy", "is_cares", "nonpayment", "notes")


detainer_warrant_schema = DetainerWarrantSchema()
detainer_warrants_schema = DetainerWarrantSchema(many=True)
