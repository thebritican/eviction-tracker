from .models import db
from .models import Attorney, Courtroom, Defendant, DetainerWarrant, District, Judge, Judgement, Plaintiff, detainer_warrant_defendants
from .util import get_or_create, normalize
from sqlalchemy.exc import IntegrityError, InternalError
from sqlalchemy.dialects.postgresql import insert
from decimal import Decimal
from datetime import date

COURT_DATE = "Court Date"
DOCKET_ID = "Docket #"
COURTROOM = "Courtroom"
PLAINTIFF = "Plaintiff"
PLAINTIFF_ATTORNEY = "Pltf Lawyer"
DEFENDANT = "Defendant"
DEFENDANT_ATTORNEY = "Def Lawyer"
DEFENDANT_ADDRESS = "Def. Address"
REASON = "Reason"
AMOUNT = "Amount"
MEDIATION_LETTER = "\"Mediation Letter\""
NOTES = "Notes (anything unusual on detainer or in "
JUDGEMENT = "Judgement"
JUDGE = "Judge"
JUDGEMENT_BASIS = "Judgement Basis"


def extract_dismissal_basis(outcome, basis):
    if basis == "ftp" or basis == "failure to prosecute":
        return "FAILURE_TO_PROSECUTE"
    elif basis == "fifod" or basis == "finding in favor of defendant":
        return "FINDING_IN_FAVOR_OF_DEFENDANT"
    elif outcome == "non-suit":
        if basis == "default" or basis == "":
            return "NON_SUIT_BY_PLAINTIFF"
        else:
            return None


def _from_spreadsheet(defaults, court_date, raw_judgement):
    judgement = {k: normalize(v) for k, v in raw_judgement.items()}

    docket_id = judgement[DOCKET_ID]

    if not docket_id:
        return

    warrant, _ = get_or_create(db.session, DetainerWarrant,
                               docket_id=docket_id, defaults={
                                   'status_id': 1, 'file_date': date.today()}
                               )

    plaintiff_attorney = None
    if judgement[PLAINTIFF_ATTORNEY]:
        plaintiff_attorney, _ = get_or_create(
            db.session, Attorney, name=judgement[PLAINTIFF_ATTORNEY], defaults=defaults)

    defendant_attorney = None
    if judgement[DEFENDANT_ATTORNEY]:
        defendant_attorney, _ = get_or_create(
            db.session, Attorney, name=judgement[DEFENDANT_ATTORNEY], defaults=defaults)

    plaintiff = None
    if judgement[PLAINTIFF]:
        plaintiff, _ = get_or_create(
            db.session, Plaintiff, name=judgement[PLAINTIFF], defaults=defaults)

    courtroom = None
    if judgement[COURTROOM]:
        courtroom, _ = get_or_create(
            db.session, Courtroom, name=judgement[COURTROOM], defaults=defaults)

    judge = None
    if judgement[JUDGE]:
        judge, _ = get_or_create(
            db.session, Judge, name=judgement[JUDGE], defaults=defaults)

    defendant_address = judgement[DEFENDANT_ADDRESS]

    awards_possession, awards_fees, in_favor_of = None, None, None
    outcome = judgement[JUDGEMENT].lower() if judgement[JUDGEMENT] else None
    if outcome:
        in_favor_of = 'PLAINTIFF' if 'poss' in outcome or 'fees' in outcome else 'DEFENDANT'
        awards_possession = 'poss' in outcome
        try:
            awards_fees = Decimal(str(judgement[AMOUNT]).replace(
                '$', '').replace(',', '')) if 'fees' in outcome and judgement[AMOUNT] else None
        except KeyError:
            awards_fees = Decimal(str(judgement["Amount Awarded"]).replace(
                '$', '').replace(',', '')) if 'fees' in outcome and judgement["Amount Awarded"] else None

    basis = judgement[JUDGEMENT_BASIS].lower(
    ) if judgement[JUDGEMENT_BASIS] else None

    mediation_letter = judgement[MEDIATION_LETTER].lower(
    ) == 'yes' if judgement[MEDIATION_LETTER] else None
    dismissal_basis = extract_dismissal_basis(
        outcome, basis)
    notes = judgement[NOTES]

    judgement_values = dict(
        detainer_warrant_id=warrant.docket_id,
        court_date=court_date,
        courtroom_id=courtroom.id if courtroom else None,
        plaintiff_id=plaintiff.id if plaintiff else None,
        plaintiff_attorney_id=plaintiff_attorney.id if plaintiff_attorney else None,
        judge_id=judge.id if judge else None,
        defendant_attorney_id=defendant_attorney.id if defendant_attorney else None,
        defendant_address=defendant_address,
        in_favor_of_id=Judgement.parties[in_favor_of] if in_favor_of else None,
        awards_possession=awards_possession,
        awards_fees=awards_fees,
        mediation_letter=mediation_letter,
        dismissal_basis_id=Judgement.dismissal_bases[dismissal_basis] if dismissal_basis else None,
        notes=notes,
    )

    insert_stmt = insert(Judgement).values(
        **judgement_values
    )

    do_update_stmt = insert_stmt.on_conflict_do_update(
        constraint=Judgement.__table__.primary_key,
        set_=judgement_values
    )

    db.session.execute(do_update_stmt)
    db.session.commit()


def from_spreadsheet(judgements):
    district, _ = get_or_create(db.session, District, name="Davidson County")

    db.session.add(district)
    db.session.commit()

    defaults = {'district': district}

    court_date = None
    for judgement in judgements:
        court_date = judgement[COURT_DATE] if judgement[COURT_DATE] else court_date
        _from_spreadsheet(defaults, court_date, judgement)


def _from_dw_sheet_row(raw_warrant):
    warrant = {k: normalize(v) for k, v in raw_warrant.items()}

    dw = db.session.query(DetainerWarrant).get(warrant["Docket #"])

    if not dw:
        print('no existing detainer warrant')
        return

    outcome = warrant['Judgement'].lower() if warrant['Judgement'] else None
    if outcome and len(dw._judgements) == 0:
        in_favor_of = 'PLAINTIFF' if 'poss' in outcome or 'fees' in outcome else 'DEFENDANT'
        awards_possession = 'poss' in outcome
        awards_fees = dw.amount_claimed if 'fees' in outcome or 'payment' in outcome else None

        judgement = Judgement.create(
            detainer_warrant_id=dw.docket_id,
            in_favor_of_id=Judgement.parties[in_favor_of],
            awards_possession=awards_possession,
            awards_fees=awards_fees
        )

        db.session.add(judgement)
        dw._judgements = dw._judgements + [judgement]
        db.session.add(dw)
        db.session.commit()


def from_dw_sheet(warrants):
    for warrant in warrants:
        _from_dw_sheet_row(warrant)
