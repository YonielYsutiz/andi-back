from flask import Blueprint, request, jsonify
import pandas as pd
import os 
from schemas.company_schemas import CompanyCreate, CompanyResponse,CompanyDelete
from werkzeug.utils import secure_filename
from models.entities.Company import Company
from pydantic import ValidationError
from db_config import db


company_routes = Blueprint('company_routes', __name__, url_prefix='/companies')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def import_companies_from_excel(file_path):
    try: 
        df = pd.read_excel(file_path)
        
        df = df.where(pd.notna(df), None)
        for _, row in df.iterrows():
            company = Company(
                nit= row['NIT'],
                name_company= row['Nombre Empresa'],
                sector = row['SECTOR']
            )

            db.session.add(company)

        db.session.commit()
        return("Datos importas exitosamente")


    except Exception as e:
        db.session.rollback()
        return(f"Error al importar datos: {e}")

@company_routes.route('/excel_company', methods=['POST'])

def excel_company():
    if 'file' not in request.files:
        return jsonify({"error": 'No se envio ningun archivo'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error", "Nombre de archivo vacio"}), 400
    
    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        response =  import_companies_from_excel(filepath)
        return jsonify(response), 200
    
    return jsonify({"error": "Formato de archivo no permitido"}), 400

@company_routes.route('/company_register', methods=['POST'])

def company_excel():
    try:
        company_data = CompanyCreate(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    existing_company = Company.query.filter_by(nit=company_data.nit).first()
    if existing_company:
        return jsonify({"Error": "Empresa ya registrada"}), 400
    
    company = Company(
        nit = company_data.nit,
        name_company = company_data.name_company,
        sector = company_data.sector
    )

    try:
        db.session.add(company)
        db.session.commit()

        return jsonify({
            "message": "Empresa registrada con exito",
            "nit": company.nit,
            "name_company": company.name_company,
            "sector": company.sector
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar empresa: {e}")
        return jsonify({"error": "Error al registrar empresa"}), 500
    
@company_routes.route('/all-companies', methods=['GET'])
def all_companies():

    nit = request.args.get('nit')
    name_company = request.args.get('name_company')
    sector = request.args.get('sector')

    query = Company.query

    if nit:
        query = query.filter(Company.nit.ilike(f"%{nit}%"))
    if name_company:
        query = query.filter(Company.name_company.ilike(f"%{name_company}%"))
    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))


    companies = query.all()
    result = [CompanyResponse.model_validate(company) for company in companies]
    return jsonify([company.model_dump() for company in result])
    


@company_routes.route('/find-company/<int:company_id>', methods=['GET'])

def findCompany(company_id):
    company = Company.query.get(company_id)
    
    if company is None: 
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    try:
        company_data = CompanyResponse.model_validate(company)
        return jsonify(company_data.model_dump())
    except ValidationError as e:
        print(f"Error al validar datos de la empresa: {e}")
        return jsonify({"error": "Error al validar datos de la empresa"}), 500
    
@company_routes.route('/update-company/<int:company_id>', methods=['PUT'])
def UpdateCompany(company_id):
    data = request.get_json()

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    if 'nit' in data:
        company.nit = data['nit']
    if 'name_company' in data:
        company.name_company = data['name_company']
    if 'sector' in data:
        company.sector = data['sector']
    
    try: 
        db.session.add(company)
        db.session.commit()
        return jsonify({"message": "Empresa actualizada correctamente", "updated_fields":{key: data[key] for key in data if key in ["nit", "name_company", "sector"]}})
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar empresa: {e}")
        return jsonify({"error": "Error al actualizar empresa"}), 400

@company_routes.route('/delete-company/<int:company_id>', methods = ['DELETE'])

def deleteCompany(company_id):
    
    company = Company.query.get(company_id)
    
    if not company:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    company_id_delete = company.id
    
    try: 
        db.session.delete(company)
        db.session.commit()
        
        response = CompanyDelete(
            message="Empresa eliminada correctamente",
            delete_company_id=company_id_delete
        )
        return jsonify(response.model_dump()), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar empresa: {e}")
        return jsonify({"error": "Error al eliminar empresa"}), 400
    
    