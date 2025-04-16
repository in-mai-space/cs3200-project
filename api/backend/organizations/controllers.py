from http import HTTPStatus
from backend.utilities.pagination import validate_pagination
from backend.validators.organizations import OrganizationSchema, OrganizationContactSchema
from backend.validators.search import validate_search_params
from backend.organizations.transactions import (
    create_organization,
    get_programs_by_organization_id, 
    insert_program, 
    get_organization_by_id, 
    delete_organization_by_id, 
    update_organization_by_id,
    create_org_contact,
    update_org_contact,
    get_organization_contact,
    delete_organization_contact,
    search_org
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from flask import Blueprint, request, jsonify, Response
from backend.validators.programs import ProgramCreateSchema

organizations = Blueprint('organizations', __name__)

#------------------------------------------------------------
# Create a program for an organization
@organizations.route('/<string:id>/programs', methods=['POST'])
def create_program(id: str) -> tuple[Response, int]:
    try:
        validate_uuid(id)
        program_schema = ProgramCreateSchema()
        data = program_schema.load(request.json)

        insert_program(id, data)
        return jsonify({ "message": "Program created successfully" }), HTTPStatus.CREATED
    
    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get all programs for an organization
@organizations.route('/<string:id>/programs', methods=['GET'])
def get_programs(id: str) -> tuple[Response, int]:
    try:
        validate_uuid(id)
        page, limit = validate_pagination()
        search_query = request.args.get('search_query')
        programs = get_programs_by_organization_id(id, page, limit, search_query)
        return jsonify(programs), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Create an organization
@organizations.route('', methods=['POST'])
def create_organizations()  -> tuple[Response, int]:
    try:
        organizations_schema = OrganizationSchema()
        data = organizations_schema.load(request.json)
        result = create_organization(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get an organization
@organizations.route('/<string:organization_id>', methods=['GET'])       
def get_organization(organization_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        organization = get_organization_by_id(organization_id)
        return jsonify(organization), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Update an organization
@organizations.route('/<string:organization_id>', methods=['PUT'])       
def update_organization(organization_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        organizations_schema = OrganizationSchema()
        data = organizations_schema.load(request.json)
        result = update_organization_by_id(organization_id, data)
        return jsonify(result), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Delete an organization
@organizations.route('/<string:organization_id>', methods=['DELETE'])       
def delete_organization(organization_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        delete_organization_by_id(organization_id)
        return jsonify({"message": "Organization deleted successfully"}), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Create organization contact
@organizations.route('/<string:organization_id>', methods=['POST'])
def create_org_contacts(organization_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        organizations_contact_schema = OrganizationContactSchema()
        data = organizations_contact_schema.load(request.json)
        new_organization_contact = create_org_contact(organization_id, data)
        return jsonify(new_organization_contact), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Update organization contact
@organizations.route('/<string:organization_id>/<string:contact_id>', methods=['PUT'])       
def update_org_contacts(organization_id: str, contact_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        validate_uuid(contact_id)
        organizations_contact_schema = OrganizationContactSchema()
        data = organizations_contact_schema.load(request.json)
        updated_contact = update_org_contact(contact_id, data)
        return jsonify(updated_contact), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get organization contact
@organizations.route('/<string:organization_id>/<string:contact_id>', methods=['GET'])
def get_org_contacts(organization_id: str, contact_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        validate_uuid(contact_id)
        result = get_organization_contact(contact_id)
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Delete organization contact
@organizations.route('/<string:organization_id>/<string:contact_id>', methods=['DELETE'])
def delete_org_contacts(organization_id: str, contact_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(organization_id)
        validate_uuid(contact_id)
        delete_organization_contact(contact_id)
        return jsonify({"message": "Organization deleted successfully"}), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Search for organizations
@organizations.route('', methods=['GET'], strict_slashes=False)
def search_organization() -> tuple[Response, int]:
    try:
        params = validate_search_params()
        results = search_org(params)
        return jsonify(results), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
