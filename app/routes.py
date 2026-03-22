from flask import Blueprint, jsonify
from app.fraud_detection import detect_fraud

routes = Blueprint('routes', __name__)

@routes.route('/fraud-alerts', methods=['GET'])
def fraud_alerts():
    result = detect_fraud()
    return jsonify(result)

from flask import request
from app.db import get_connection

@routes.route('/transaction', methods=['POST'])
def transaction():
    data = request.json

    account_id = data['account_id']
    txn_type = data['type']
    amount = data['amount']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.callproc('process_transaction', [account_id, txn_type, amount])

    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction processed"})

@routes.route('/upload-kyc', methods=['POST'])
def upload_kyc():
    file = request.files['file']
    customer_id = request.form['customer_id']
    doc_type = request.form['document_type']

    file_data = file.read()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO kyc_documents (customer_id, document_type, document_blob)
        VALUES (:1, :2, :3)
    """, (customer_id, doc_type, file_data))

    conn.commit()
    conn.close()

    return jsonify({"message": "KYC uploaded"})