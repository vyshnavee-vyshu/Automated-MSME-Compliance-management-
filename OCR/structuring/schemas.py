"""Pydantic schemas for the two compliance document families this
pipeline extracts into. Every field is optional — a document rarely
carries all of them, and the LLM must never guess a value it can't
find in the OCR text; missing fields stay null.
"""
from typing import Optional

from pydantic import BaseModel


class LabourComplianceRecord(BaseModel):
    establishment_name: Optional[str] = None
    establishment_registration_number: Optional[str] = None
    employer_owner_name: Optional[str] = None
    establishment_address: Optional[str] = None
    nature_of_business: Optional[str] = None
    establishment_type: Optional[str] = None
    date_of_commencement: Optional[str] = None
    number_of_employees: Optional[str] = None
    employee_worker_details: Optional[str] = None
    employment_category: Optional[str] = None
    wage_salary_details: Optional[str] = None
    working_hours: Optional[str] = None
    attendance_working_days: Optional[str] = None
    overtime_details: Optional[str] = None
    leave_details: Optional[str] = None
    minimum_wage_compliance: Optional[str] = None
    epf_uan_details: Optional[str] = None
    epf_contribution: Optional[str] = None
    esi_details: Optional[str] = None
    esi_contribution: Optional[str] = None
    professional_tax_details: Optional[str] = None
    labour_welfare_fund_details: Optional[str] = None
    bonus_details: Optional[str] = None
    gratuity_details: Optional[str] = None
    maternity_benefit_details: Optional[str] = None
    contractor_details: Optional[str] = None
    labour_license_registration_details: Optional[str] = None
    applicable_labour_act: Optional[str] = None
    compliance_return_period: Optional[str] = None
    return_filing_details: Optional[str] = None
    challan_payment_details: Optional[str] = None
    date_of_submission: Optional[str] = None
    acknowledgement_reference_number: Optional[str] = None
    supporting_documents: Optional[str] = None
    compliance_status: Optional[str] = None


class TaxationComplianceRecord(BaseModel):
    business_company_name: Optional[str] = None
    pan: Optional[str] = None
    tan: Optional[str] = None
    gstin: Optional[str] = None
    business_type: Optional[str] = None
    registered_business_address: Optional[str] = None
    date_of_registration: Optional[str] = None
    financial_year: Optional[str] = None
    assessment_year: Optional[str] = None
    taxpayer_type: Optional[str] = None
    turnover: Optional[str] = None
    total_income: Optional[str] = None
    taxable_income: Optional[str] = None
    tax_liability: Optional[str] = None
    advance_tax_paid: Optional[str] = None
    self_assessment_tax_paid: Optional[str] = None
    tds_details: Optional[str] = None
    tds_deducted: Optional[str] = None
    tds_deposited: Optional[str] = None
    tds_return_details: Optional[str] = None
    gst_sales_outward_supplies: Optional[str] = None
    gst_purchases_inward_supplies: Optional[str] = None
    input_tax_credit_itc: Optional[str] = None
    output_gst_liability: Optional[str] = None
    gst_tax_paid: Optional[str] = None
    gst_return_details: Optional[str] = None
    tax_payment_challan_details: Optional[str] = None
    return_filing_period: Optional[str] = None
    return_filing_date: Optional[str] = None
    acknowledgement_number: Optional[str] = None
    tax_demand_outstanding_amount: Optional[str] = None
    refund_details: Optional[str] = None
    supporting_documents: Optional[str] = None


SCHEMAS = {
    "labour": LabourComplianceRecord,
    "taxation": TaxationComplianceRecord,
}
