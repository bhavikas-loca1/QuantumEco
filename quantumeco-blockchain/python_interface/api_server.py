"""
HTTP API Server for Blockchain Operations

Provides HTTP interface bridging Python 3.12 backend with Python 3.7-3.11 blockchain operations.
This server handles the version compatibility gap for web3.py and solcx dependencies.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

from .blockchain_service import ABI_CACHE, BlockchainService, DEFAULT_CONFIG, CONTRACT_ADDRESSES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

def initialize_blockchain_interface(config=None):
    """Initialize the blockchain interface with custom configuration"""
    global DEFAULT_CONFIG
    if config:
        DEFAULT_CONFIG.update(config)
    
    print(f"🚀 QuantumEco Blockchain Interface initialized")
    print(f"📡 Ganache URL: {DEFAULT_CONFIG['ganache_url']}")
    print(f"🔌 API Port: {DEFAULT_CONFIG['api_port']}")
    
    return DEFAULT_CONFIG

def get_health_status():
    """Get overall health status of blockchain interface"""
    try:
        service = BlockchainService()
        return {
            "status": "healthy",
            "version": 1,
            "ganache_connected": service.is_connected(),
            "contracts_loaded": len(ABI_CACHE) > 0,
            "api_running": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "version": 1,
            "error": str(e)
        }

# Export all main components
__all__ = [
    "BlockchainService",
    "ContractInterface", 
    "Web3Utils",
    "blockchain_api",
    "initialize_blockchain_interface",
    "get_health_status",
    "DEFAULT_CONFIG",
    "CONTRACT_ADDRESSES"
]

# Global blockchain service instance
blockchain_service = None
server_metrics = {
    "requests_processed": 0,
    "certificates_created": 0,
    "ett_tokens_created": 0,
    "carbon_credits_issued": 0,
    "errors_encountered": 0,
    "uptime_start": time.time()
}

def init_blockchain_service():
    """Initialize blockchain service"""
    global blockchain_service
    try:
        # Initialize blockchain interface
        config = initialize_blockchain_interface()
        
        # Create blockchain service instance
        blockchain_service = BlockchainService(config)
        
        logger.info("✅ Blockchain API server initialized")
        return True
        
    except Exception as e:
        logger.error(f"❌ Blockchain service initialization failed: {str(e)}")
        return False

# ===== API ENDPOINTS =====

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Get overall health status
        health_status = get_health_status()
        
        # Add API server specific metrics
        health_status.update({
            "api_server": {
                "status": "healthy",
                "requests_processed": server_metrics["requests_processed"],
                "uptime_seconds": time.time() - server_metrics["uptime_start"],
                "blockchain_service_connected": blockchain_service.is_connected() if blockchain_service else False
            }
        })
        
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503

@app.route('/blockchain/certificate', methods=['POST'])
def create_certificate():
    """Create blockchain delivery certificate"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "success": False,
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get request data
        certificate_data = request.get_json()
        if not certificate_data:
            return jsonify({
                "success": False,
                "error": "No certificate data provided"
            }), 400
        
        # Validate required fields
        required_fields = ["route_id", "vehicle_id", "carbon_saved", "cost_saved", "distance_km", "optimization_score"]
        for field in required_fields:
            if field not in certificate_data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Create certificate using blockchain service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                blockchain_service.create_delivery_certificate(certificate_data)
            )
        finally:
            loop.close()
        
        if result.get("success"):
            server_metrics["certificates_created"] += 1
            return jsonify(result), 200
        else:
            server_metrics["errors_encountered"] += 1
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Certificate creation failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/blockchain/certificate/<certificate_id>', methods=['GET'])
def get_certificate(certificate_id):
    """Get certificate details and verification status"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "verified": False,
                "error": "Blockchain service not initialized"
            }), 503
        
        # Verify certificate
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                blockchain_service.verify_certificate(certificate_id)
            )
        finally:
            loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Certificate verification failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "verified": False,
            "certificate_id": certificate_id,
            "error": str(e)
        }), 500

@app.route('/blockchain/verify', methods=['POST'])
def verify_certificate():
    """Verify certificate authenticity"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "verified": False,
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get request data
        verify_data = request.get_json()
        if not verify_data or "certificate_id" not in verify_data:
            return jsonify({
                "verified": False,
                "error": "Certificate ID required"
            }), 400
        
        certificate_id = verify_data["certificate_id"]
        
        # Verify certificate
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                blockchain_service.verify_certificate(certificate_id)
            )
        finally:
            loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Certificate verification failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "verified": False,
            "error": str(e)
        }), 500

@app.route('/blockchain/ett/create', methods=['POST'])
def create_ett():
    """Create Environmental Trust Token"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "success": False,
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get request data
        ett_data = request.get_json()
        if not ett_data:
            return jsonify({
                "success": False,
                "error": "No ETT data provided"
            }), 400
        
        # Validate required fields
        required_fields = ["route_id", "trust_score", "carbon_impact", "sustainability_rating"]
        for field in required_fields:
            if field not in ett_data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Create ETT using blockchain service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                blockchain_service.create_environmental_trust_token(ett_data)
            )
        finally:
            loop.close()
        
        if result.get("success"):
            server_metrics["ett_tokens_created"] += 1
            return jsonify(result), 200
        else:
            server_metrics["errors_encountered"] += 1
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"ETT creation failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/blockchain/carbon-credit', methods=['POST'])
def create_carbon_credit():
    """Create tradeable carbon credit"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "success": False,
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get request data
        credit_data = request.get_json()
        if not credit_data:
            return jsonify({
                "success": False,
                "error": "No carbon credit data provided"
            }), 400
        
        # Validate required fields
        required_fields = ["route_id", "carbon_amount", "value_usd"]
        for field in required_fields:
            if field not in credit_data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Create carbon credit using blockchain service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                blockchain_service.create_carbon_credit(credit_data)
            )
        finally:
            loop.close()
        
        if result.get("success"):
            server_metrics["carbon_credits_issued"] += 1
            return jsonify(result), 200
        else:
            server_metrics["errors_encountered"] += 1
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Carbon credit creation failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/blockchain/transaction/<tx_hash>', methods=['GET'])
def get_transaction_details(tx_hash):
    """Get blockchain transaction details"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get transaction details
        result = blockchain_service.get_transaction_details(tx_hash)
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Transaction details failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "error": str(e),
            "transaction_hash": tx_hash
        }), 500

@app.route('/blockchain/certificates/recent', methods=['GET'])
def get_recent_certificates():
    """Get recently created certificates"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "certificates": [],
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get query parameters
        limit = int(request.args.get('limit', 10))
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
        
        # Get recent certificates
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            certificates = loop.run_until_complete(
                blockchain_service.get_recent_certificates(limit)
            )
        finally:
            loop.close()
        
        return jsonify({
            "certificates": certificates,
            "count": len(certificates),
            "limit": limit
        }), 200
        
    except Exception as e:
        logger.error(f"Recent certificates failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "certificates": [],
            "error": str(e)
        }), 500

@app.route('/blockchain/explorer', methods=['GET'])
def blockchain_explorer():
    """Get blockchain network statistics and explorer data"""
    try:
        server_metrics["requests_processed"] += 1
        
        if not blockchain_service:
            return jsonify({
                "error": "Blockchain service not initialized"
            }), 503
        
        # Get network statistics
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            stats = loop.run_until_complete(
                blockchain_service.get_network_statistics()
            )
        finally:
            loop.close()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Blockchain explorer failed: {str(e)}")
        server_metrics["errors_encountered"] += 1
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get API server metrics"""
    try:
        uptime = time.time() - server_metrics["uptime_start"]
        
        metrics = {
            "server_metrics": {
                **server_metrics,
                "uptime_seconds": uptime,
                "requests_per_minute": server_metrics["requests_processed"] / max(uptime / 60, 1),
                "error_rate": server_metrics["errors_encountered"] / max(server_metrics["requests_processed"], 1)
            },
            "blockchain_service_metrics": blockchain_service.metrics if blockchain_service else {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Metrics failed: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get comprehensive server status"""
    try:
        uptime = time.time() - server_metrics["uptime_start"]
        
        status = {
            "server": {
                "status": "running",
                "version": "1.0.0",
                "uptime_seconds": uptime,
                "requests_processed": server_metrics["requests_processed"]
            },
            "blockchain_service": {
                "initialized": blockchain_service is not None,
                "connected": blockchain_service.is_connected() if blockchain_service else False,
                "health": blockchain_service.health_check() if blockchain_service else {"status": "not_initialized"}
            },
            "endpoints": [
                "/health",
                "/blockchain/certificate",
                "/blockchain/certificate/<id>",
                "/blockchain/verify",
                "/blockchain/ett/create",
                "/blockchain/carbon-credit",
                "/blockchain/transaction/<hash>",
                "/blockchain/certificates/recent",
                "/blockchain/explorer",
                "/metrics",
                "/status"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/health", "/blockchain/certificate", "/blockchain/verify",
            "/blockchain/explorer", "/metrics", "/status"
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "Check the HTTP method for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    server_metrics["errors_encountered"] += 1
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

# ===== SERVER STARTUP =====

def run_server(host='0.0.0.0', port=8546, debug=False):
    """Run the blockchain API server"""
    logger.info(f"🚀 Starting QuantumEco Blockchain API Server...")
    logger.info(f"🌐 Server will run on http://{host}:{port}")
    logger.info(f"📚 Available endpoints:")
    logger.info(f"   - GET  /health")
    logger.info(f"   - POST /blockchain/certificate")
    logger.info(f"   - GET  /blockchain/certificate/<id>")
    logger.info(f"   - POST /blockchain/verify")
    logger.info(f"   - POST /blockchain/ett/create")
    logger.info(f"   - POST /blockchain/carbon-credit")
    logger.info(f"   - GET  /blockchain/transaction/<hash>")
    logger.info(f"   - GET  /blockchain/certificates/recent")
    logger.info(f"   - GET  /blockchain/explorer")
    logger.info(f"   - GET  /metrics")
    logger.info(f"   - GET  /status")
    
    # Initialize blockchain service
    if init_blockchain_service():
        logger.info("✅ Blockchain service ready")
    else:
        logger.warning("⚠️ Blockchain service failed to initialize - running in mock mode")
    
    # Run Flask server
    app.run(host=host, port=port, debug=debug, threaded=True)

# ===== STANDALONE EXECUTION =====

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='QuantumEco Blockchain API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8546, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    try:
        run_server(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {str(e)}")
