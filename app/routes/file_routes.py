from flask import Blueprint, render_template, request, flash, jsonify
from app.services.file_service import FileService
from app.services.optimization_service import OptimizationService
from decimal import Decimal

file_bp = Blueprint('file', __name__)
file_service = FileService()
optimization_service = OptimizationService()

def validate_prices(cost, best_guess_price, max_price):
    errors = []
    
    # Convert to Decimal for precise decimal arithmetic
    cost = Decimal(str(cost))
    best_guess_price = Decimal(str(best_guess_price))
    max_price = Decimal(str(max_price))
    
    # Check if prices are positive
    if cost <= 0:
        errors.append("Cost must be greater than 0")
    if best_guess_price <= 0:
        errors.append("Best-guess price must be greater than 0")
    if max_price <= 0:
        errors.append("Maximum price must be greater than 0")
    
    # Check if prices are in logical order
    if cost >= best_guess_price:
        errors.append("Cost must be less than best-guess price")
    if best_guess_price >= max_price:
        errors.append("Best-guess price must be less than maximum price")
    
    # Check if there's reasonable profit margin
    min_margin = Decimal('0.05')  # 5% minimum margin
    if (best_guess_price - cost) / cost < min_margin:
        errors.append("Best-guess price must allow for at least 5% profit margin")
    
    return errors

@file_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get form data
        try:
            cost = float(request.form['cost'])
            best_guess_price = float(request.form['best_guess_price'])
            max_price = float(request.form['max_price'])
        except ValueError:
            return "Please enter valid numbers for all price fields"
        
        # Validate prices
        errors = validate_prices(cost, best_guess_price, max_price)
        if errors:
            return "<br>".join(errors)  # In real app, use proper error display
        
        # Handle file upload
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
            
        if file and file_service.allowed_file(file.filename):
            data_info = file_service.process_file(file)
            
            # Run optimization with the monthly averages
            result = optimization_service.optimize(
                monthly_volumes=data_info['monthly_averages'],
                cost=cost,
                best_guess_price=best_guess_price,
                max_price=max_price
            )
            
            # Combine data_info and optimization results
            return render_template('result.html', 
                                data_info=data_info,
                                optimization=result,
                                cost=cost,
                                best_guess_price=best_guess_price,
                                max_price=max_price)
            
    return render_template('upload.html')

@file_bp.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        # Get JSON data
        data = request.get_json()
        
        cost = float(data['cost'])
        best_guess_price = float(data['best_guess_price'])
        max_price = float(data['max_price'])
        monthly_volumes = data['monthly_volumes']  # List of 12 average volumes
        
        # Validate prices
        errors = validate_prices(cost, best_guess_price, max_price)
        if errors:
            return jsonify({"errors": errors}), 400
            
        # Run optimization
        result = optimization_service.optimize(
            monthly_volumes=monthly_volumes,
            cost=cost,
            best_guess_price=best_guess_price,
            max_price=max_price
        )
        
        return jsonify(result)
        
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": "Invalid numeric value provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500 