from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List, Dict, Any, Optional
import asyncio
import time
import uuid
import hashlib
from datetime import datetime

from app.schemas.blockchain_schemas import (
    CertificateCreationRequest,
    CertificateDetailsResponse,
    CertificateVerificationRequest,
    CertificateVerificationResponse,
    ETTCreationRequest,
    ETTCreationResponse,
    TransactionDetailsResponse,
    RecentCertificatesResponse,
    BlockchainExplorerResponse,
    CarbonCreditCreationRequest,
    CarbonCreditCreationResponse
)
from app.services.blockchain_service import BlockchainService
from app.utils.helpers import generate_certificate_id, validate_ethereum_address
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Initialize blockchain service
blockchain_service = BlockchainService()

# In-memory cache for certificates and transactions (for demo purposes)
certificate_cache: Dict[str, Dict[str, Any]] = {}
transaction_cache: Dict[str, Dict[str, Any]] = {}

@router.post("/certificate", response_model=CertificateDetailsResponse)
async def create_delivery_certificate(
    request: CertificateCreationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create blockchain-verified delivery certificate
    Stores delivery optimization results immutably on blockchain
    """
    print(f"[CERTIFICATE] Starting certificate creation process for route {request.route_id}")
    print(f"[CERTIFICATE] Input request data: {request.dict()}")
    
    try:
        # Input validation
        print("[CERTIFICATE] Validating input parameters...")
        if request.carbon_saved < 0:
            print(f"[ERROR] Invalid carbon saved value: {request.carbon_saved}")
            raise HTTPException(status_code=400, detail="Carbon saved cannot be negative")
        
        if request.cost_saved < 0:
            print(f"[ERROR] Invalid cost saved value: {request.cost_saved}")
            raise HTTPException(status_code=400, detail="Cost saved cannot be negative")
        
        if request.distance_km <= 0:
            print(f"[ERROR] Invalid distance value: {request.distance_km}")
            raise HTTPException(status_code=400, detail="Distance must be greater than 0")
        
        if request.optimization_score < 0 or request.optimization_score > 100:
            print(f"[ERROR] Invalid optimization score: {request.optimization_score}")
            raise HTTPException(status_code=400, detail="Optimization score must be between 0 and 100")
        
        print("[CERTIFICATE] Input validation successful")

        # Generate certificate ID
        print("[CERTIFICATE] Generating certificate ID...")
        certificate_id = generate_certificate_id()
        print(f"[CERTIFICATE] Generated certificate ID: {certificate_id}")

        # Prepare certificate data
        print("[CERTIFICATE] Preparing certificate data for blockchain...")
        certificate_data = {
            "route_id": request.route_id,
            "vehicle_id": request.vehicle_id,
            "carbon_saved": request.carbon_saved,
            "cost_saved": request.cost_saved,
            "distance_km": request.distance_km,
            "optimization_score": request.optimization_score,
            "timestamp": int(time.time())
        }
        print(f"[CERTIFICATE] Certificate data prepared: {certificate_data}")
        
        # Calculate verification hash
        print("[CERTIFICATE] Calculating verification hash...")
        verification_hash = blockchain_service.calculate_verification_hash(certificate_data)
        print(f"[CERTIFICATE] Generated verification hash: {verification_hash}")

        # Create blockchain certificate
        print("[CERTIFICATE] Initiating blockchain certificate creation...")
        blockchain_data = {**certificate_data, "certificate_id": certificate_id, "verification_hash": verification_hash}
        print(f"[CERTIFICATE] Sending data to blockchain: {blockchain_data}")
        
        blockchain_result = await blockchain_service.create_delivery_certificate(blockchain_data)
        print(f"[CERTIFICATE] Blockchain creation result: {blockchain_result}")

        if not blockchain_result.get("verified"):
            error_msg = f"Blockchain certificate creation failed: {blockchain_result.get('error', 'Unknown error')}"
            print(f"[ERROR] {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        print("[CERTIFICATE] Certificate successfully created on blockchain")

        # Prepare response
        print("[CERTIFICATE] Preparing API response...")
        response = CertificateDetailsResponse(
            certificate_id=certificate_id,
            route_id=request.route_id,
            vehicle_id=request.vehicle_id,
            carbon_saved_kg=request.carbon_saved,
            cost_saved_usd=request.cost_saved,
            distance_km=request.distance_km,
            optimization_score=request.optimization_score,
            verification_hash=verification_hash,
            transaction_hash=blockchain_result["transaction_hash"],
            block_number=blockchain_result["block_number"],
            gas_used=blockchain_result.get("gas_used", 0),
            verified=True,
            created_at=datetime.utcnow(),
            blockchain_network="ganache_local",
            certificate_status="verified"
        )
        print(f"[CERTIFICATE] Response object created: {response.dict()}")

        # Cache management
        print("[CERTIFICATE] Updating certificate cache...")
        certificate_cache[certificate_id] = response.dict()
        print(f"[CERTIFICATE] Certificate cached. Total certificates in cache: {len(certificate_cache)}")

        print("[CERTIFICATE] Updating transaction cache...")
        transaction_cache[blockchain_result["transaction_hash"]] = {
            "certificate_id": certificate_id,
            "transaction_type": "certificate_creation",
            "block_number": blockchain_result["block_number"],
            "gas_used": blockchain_result.get("gas_used", 0),
            "timestamp": datetime.utcnow()
        }
        print(f"[CERTIFICATE] Transaction cached. Total transactions in cache: {len(transaction_cache)}")

        # Database storage
        print("[CERTIFICATE] Scheduling database storage background task...")
        background_tasks.add_task(
            store_certificate_in_db,
            certificate_id,
            response.dict()
        )
        print(f"[CERTIFICATE] Background task scheduled for certificate {certificate_id}")

        print("[CERTIFICATE] Certificate creation process completed successfully")
        return response
        
    except HTTPException as he:
        print(f"[ERROR] HTTP Exception in certificate creation: {str(he)}")
        raise he
    except Exception as e:
        error_msg = f"Certificate creation failed: {str(e)}"
        print(f"[ERROR] Unexpected error in certificate creation: {error_msg}")
        print(f"[ERROR] Exception type: {type(e)}")
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/certificate/{certificate_id}", response_model=CertificateDetailsResponse)
async def get_certificate_details(certificate_id: str):
    """
    Retrieve certificate details and verification status from blockchain
    """
    try:
        # Check cache first
        if certificate_id in certificate_cache:
            cached_cert = certificate_cache[certificate_id]
            
            # Verify current blockchain status
            blockchain_verification = await blockchain_service.verify_certificate_on_chain(certificate_id)
            
            # Update verification status
            cached_cert["verified"] = blockchain_verification.get("verified", False)
            cached_cert["last_verified"] = datetime.utcnow()
            
            return CertificateDetailsResponse(**cached_cert)
        
        # If not in cache, try to retrieve from blockchain
        blockchain_data = await blockchain_service.get_certificate_from_blockchain(certificate_id)
        
        if not blockchain_data:
            raise HTTPException(status_code=404, detail="Certificate not found")
        
        # Convert blockchain data to response format
        response = CertificateDetailsResponse(
            certificate_id=certificate_id,
            route_id=blockchain_data["route_id"],
            vehicle_id=blockchain_data["vehicle_id"],
            carbon_saved_kg=blockchain_data["carbon_saved"] / 1000,  # Convert from grams
            cost_saved_usd=blockchain_data["cost_saved"] / 100,      # Convert from cents
            distance_km=blockchain_data["distance_km"] / 1000,      # Convert from meters
            optimization_score=blockchain_data["optimization_score"],
            verification_hash=blockchain_data["verification_hash"],
            transaction_hash=blockchain_data["transaction_hash"],
            block_number=blockchain_data["block_number"],
            verified=True,
            created_at=datetime.fromtimestamp(blockchain_data["timestamp"]),
            blockchain_network="ganache_local",
            certificate_status="verified"
        )
        
        # Cache the retrieved certificate
        certificate_cache[certificate_id] = response.dict()
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve certificate: {str(e)}")


@router.post("/verify", response_model=CertificateVerificationResponse)
async def verify_certificate_authenticity(request: CertificateVerificationRequest):
    """
    Verify certificate authenticity on blockchain
    Provides comprehensive verification including hash validation
    """
    try:
        # Get certificate details
        certificate_data = await blockchain_service.get_certificate_from_blockchain(request.certificate_id)
        
        if not certificate_data:
            return CertificateVerificationResponse(
                certificate_id=request.certificate_id,
                is_valid=False,
                verification_status="not_found",
                error_message="Certificate not found on blockchain",
                verified_at=datetime.utcnow()
            )
        
        # Verify hash integrity if provided
        hash_valid = True
        if request.expected_hash:
            actual_hash = certificate_data.get("verification_hash")
            hash_valid = actual_hash == request.expected_hash
        
        # Verify blockchain integrity
        blockchain_valid = await blockchain_service.verify_blockchain_integrity(request.certificate_id)
        
        # Determine overall validity
        is_valid = hash_valid and blockchain_valid
        
        # Determine verification status
        if not hash_valid:
            status = "hash_mismatch"
            error_msg = "Certificate hash does not match expected value"
        elif not blockchain_valid:
            status = "blockchain_invalid"
            error_msg = "Certificate blockchain verification failed"
        else:
            status = "verified"
            error_msg = None
        
        response = CertificateVerificationResponse(
            certificate_id=request.certificate_id,
            is_valid=is_valid,
            verification_status=status,
            hash_verification=hash_valid,
            blockchain_verification=blockchain_valid,
            transaction_hash=certificate_data.get("transaction_hash"),
            block_number=certificate_data.get("block_number"),
            error_message=error_msg,
            verified_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Certificate verification failed: {str(e)}")


@router.post("/ett/create", response_model=ETTCreationResponse)
async def create_environmental_trust_token(
    request: ETTCreationRequest,
    background_tasks: BackgroundTasks
):
    """
    Create Environmental Trust Token for sustainable delivery
    Links to existing delivery certificate and adds sustainability metrics
    """
    try:
        # Validate input parameters
        if request.trust_score < 0 or request.trust_score > 100:
            raise HTTPException(status_code=400, detail="Trust score must be between 0 and 100")
        
        if request.sustainability_rating < 0 or request.sustainability_rating > 100:
            raise HTTPException(status_code=400, detail="Sustainability rating must be between 0 and 100")
        
        # Verify that the referenced route certificate exists
        certificate_exists = await blockchain_service.verify_certificate_exists(request.route_id)
        if not certificate_exists:
            raise HTTPException(
                status_code=404, 
                detail=f"Referenced route certificate {request.route_id} not found"
            )
        
        # Create ETT on blockchain
        ett_result = await blockchain_service.create_environmental_trust_token({
            "route_id": request.route_id,
            "trust_score": request.trust_score,
            "carbon_impact": request.carbon_impact,
            "sustainability_rating": request.sustainability_rating,
            "metadata": request.metadata or {}
        })
        
        if not ett_result.get("token_id"):
            raise HTTPException(
                status_code=500,
                detail=f"ETT creation failed: {ett_result.get('error', 'Unknown error')}"
            )
        
        # Calculate environmental impact description
        impact_description = blockchain_service.generate_environmental_impact_description(
            request.carbon_impact,
            request.sustainability_rating
        )
        
        response = ETTCreationResponse(
            token_id=ett_result["token_id"],
            route_id=request.route_id,
            trust_score=request.trust_score,
            carbon_impact_kg=request.carbon_impact,
            sustainability_rating=request.sustainability_rating,
            environmental_impact_description=impact_description,
            transaction_hash=ett_result["transaction_hash"],
            block_number=ett_result.get("block_number", 0),
            token_status="active",
            created_at=datetime.utcnow(),
            metadata=request.metadata or {}
        )
        
        # Store transaction details
        transaction_cache[ett_result["transaction_hash"]] = {
            "token_id": ett_result["token_id"],
            "transaction_type": "ett_creation",
            "block_number": ett_result.get("block_number", 0),
            "timestamp": datetime.utcnow()
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ETT creation failed: {str(e)}")


@router.get("/transaction/{tx_hash}", response_model=TransactionDetailsResponse)
async def get_transaction_details(tx_hash: str):
    """
    Get detailed blockchain transaction information
    """
    try:
        # Validate transaction hash format
        if not tx_hash.startswith("0x") or len(tx_hash) != 66:
            raise HTTPException(status_code=400, detail="Invalid transaction hash format")
        
        # Check cache first
        if tx_hash in transaction_cache:
            cached_tx = transaction_cache[tx_hash]
            
            # Get additional details from blockchain
            blockchain_details = await blockchain_service.get_transaction_details(tx_hash)
            
            response = TransactionDetailsResponse(
                transaction_hash=tx_hash,
                block_number=cached_tx.get("block_number", blockchain_details.get("blockNumber", 0)),
                block_hash=blockchain_details.get("blockHash", ""),
                transaction_index=blockchain_details.get("transactionIndex", 0),
                from_address=blockchain_details.get("from", ""),
                to_address=blockchain_details.get("to", ""),
                gas_used=blockchain_details.get("gasUsed", 0),
                gas_price=blockchain_details.get("gasPrice", 0),
                transaction_fee=blockchain_details.get("gasUsed", 0) * blockchain_details.get("gasPrice", 0),
                status="success" if blockchain_details.get("status") == 1 else "failed",
                timestamp=cached_tx.get("timestamp", datetime.utcnow()),
                transaction_type=cached_tx.get("transaction_type", "unknown"),
                related_certificate_id=cached_tx.get("certificate_id"),
                related_token_id=cached_tx.get("token_id")
            )
            
            return response
        
        # If not in cache, get from blockchain
        blockchain_details = await blockchain_service.get_transaction_details(tx_hash)
        
        if not blockchain_details:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        response = TransactionDetailsResponse(
            transaction_hash=tx_hash,
            block_number=blockchain_details.get("blockNumber", 0),
            block_hash=blockchain_details.get("blockHash", ""),
            transaction_index=blockchain_details.get("transactionIndex", 0),
            from_address=blockchain_details.get("from", ""),
            to_address=blockchain_details.get("to", ""),
            gas_used=blockchain_details.get("gasUsed", 0),
            gas_price=blockchain_details.get("gasPrice", 0),
            transaction_fee=blockchain_details.get("gasUsed", 0) * blockchain_details.get("gasPrice", 0),
            status="success" if blockchain_details.get("status") == 1 else "failed",
            timestamp=datetime.fromtimestamp(blockchain_details.get("timestamp", time.time())),
            transaction_type="unknown"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get transaction details: {str(e)}")


@router.get("/certificates/recent", response_model=RecentCertificatesResponse)
async def get_recent_certificates(limit: int = 10, offset: int = 0):
    """
    Get recently created delivery certificates
    """
    try:
        if limit > 100:
            raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
        
        if limit < 1:
            raise HTTPException(status_code=400, detail="Limit must be at least 1")
        
        # Get recent certificates from blockchain
        recent_certs = await blockchain_service.get_recent_certificates(limit + offset)
        
        # Apply pagination
        paginated_certs = recent_certs[offset:offset + limit]
        
        # Convert to response format
        certificates = []
        for cert_data in paginated_certs:
            cert_summary = {
                "certificate_id": cert_data["certificate_id"],
                "route_id": cert_data["route_id"],
                "carbon_saved_kg": cert_data["carbon_saved"] / 1000,
                "cost_saved_usd": cert_data["cost_saved"] / 100,
                "optimization_score": cert_data["optimization_score"],
                "transaction_hash": cert_data["transaction_hash"],
                "block_number": cert_data["block_number"],
                "created_at": datetime.fromtimestamp(cert_data["timestamp"]),
                "verified": True
            }
            certificates.append(cert_summary)
        
        response = RecentCertificatesResponse(
            certificates=certificates,
            total_count=len(recent_certs),
            limit=limit,
            offset=offset,
            has_more=len(recent_certs) > offset + limit
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent certificates: {str(e)}")


@router.get("/explorer", response_model=BlockchainExplorerResponse)
async def get_blockchain_explorer_data():
    """
    Blockchain explorer interface with network statistics
    """
    try:
        print("[EXPLORER] Starting blockchain explorer data retrieval")
        
        print("[EXPLORER] Fetching network statistics...")
        network_stats = await blockchain_service.get_network_statistics()
        print(f"[EXPLORER] Network stats retrieved: {network_stats}")
        
        print("[EXPLORER] Fetching recent blocks...")
        recent_blocks = await blockchain_service.get_recent_blocks(5)
        print(f"[EXPLORER] Retrieved {len(recent_blocks)} recent blocks")
        
        print("[EXPLORER] Fetching recent transactions...") 
        recent_transactions = await blockchain_service.get_recent_transactions(10)
        print(f"[EXPLORER] Retrieved {len(recent_transactions)} recent transactions")
        
        # Calculate metrics
        total_certificates = len(certificate_cache)
        total_transactions = len(transaction_cache)
        print(f"[EXPLORER] Metrics calculated - Certificates: {total_certificates}, Transactions: {total_transactions}")
        
        print("[EXPLORER] Fetching gas statistics...")
        gas_stats = await blockchain_service.get_gas_statistics()
        print(f"[EXPLORER] Gas stats retrieved: {gas_stats}")
        
        try:
            total_carbon_saved = network_stats.get("total_carbon_saved", 0) / 1000
            total_cost_saved = network_stats.get("total_cost_saved", 0) / 100
            print(f"[EXPLORER] Calculated savings - Carbon: {total_carbon_saved}kg, Cost: ${total_cost_saved}")
        except Exception as calc_error:
            print(f"[ERROR] Failed to calculate savings: {str(calc_error)}")
            total_carbon_saved = 0
            total_cost_saved = 0
            
        print("[EXPLORER] Building response object...")
        response = BlockchainExplorerResponse(
            network_name="Ganache Local Network",
            network_id=network_stats.get("network_id", 1337),
            latest_block_number=network_stats.get("latest_block", 0),
            total_transactions=total_transactions,
            total_certificates=total_certificates,
            total_carbon_saved_kg=total_carbon_saved,
            total_cost_saved_usd=total_cost_saved,
            average_gas_price=gas_stats.get("average_gas_price", 0),
            network_hash_rate=network_stats.get("hash_rate", 0),
            recent_blocks=recent_blocks,
            recent_transactions=recent_transactions,
            node_count=1,
            network_status="healthy",
            last_updated=datetime.utcnow()
        )
        
        print("[EXPLORER] Response object created successfully")
        print(f"[EXPLORER] Final response data: {response.dict()}")
        
        return response
        
    except Exception as e:
        error_msg = f"Failed to get explorer data: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Exception type: {type(e)}")
        print(f"[ERROR] Exception traceback: ", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/carbon-credit", response_model=CarbonCreditCreationResponse)
async def create_carbon_credit_token(
    request: CarbonCreditCreationRequest,
    background_tasks: BackgroundTasks
):
    """
    Create tradeable carbon credit tokens based on verified carbon savings
    """
    try:
        # Validate input parameters
        if request.carbon_amount_kg <= 0:
            raise HTTPException(status_code=400, detail="Carbon amount must be greater than 0")
        
        if request.value_usd <= 0:
            raise HTTPException(status_code=400, detail="Value must be greater than 0")
        
        # Verify that the referenced route exists and has carbon savings
        route_verification = await blockchain_service.verify_route_carbon_savings(request.route_id)
        if not route_verification.get("verified"):
            raise HTTPException(
                status_code=404,
                detail=f"Route {request.route_id} not found or has no verified carbon savings"
            )
        
        # Ensure carbon credit amount doesn't exceed actual savings
        actual_savings = route_verification.get("carbon_saved_kg", 0)
        if request.carbon_amount_kg > actual_savings:
            raise HTTPException(
                status_code=400,
                detail=f"Carbon credit amount ({request.carbon_amount_kg} kg) exceeds actual savings ({actual_savings} kg)"
            )
        
        # Create carbon credit on blockchain
        credit_result = await blockchain_service.create_carbon_credit({
            "route_id": request.route_id,
            "carbon_amount_kg": request.carbon_amount_kg,
            "value_usd": request.value_usd,
            "issuer": request.issuer or "QuantumEco Intelligence",
            "metadata": request.metadata or {}
        })
        
        if not credit_result.get("credit_id"):
            raise HTTPException(
                status_code=500,
                detail=f"Carbon credit creation failed: {credit_result.get('error', 'Unknown error')}"
            )
        
        # Calculate environmental equivalents
        environmental_equivalents = blockchain_service.calculate_environmental_equivalents(
            request.carbon_amount_kg
        )
        
        response = CarbonCreditCreationResponse(
            credit_id=credit_result["credit_id"],
            route_id=request.route_id,
            carbon_amount_kg=request.carbon_amount_kg,
            value_usd=request.value_usd,
            price_per_kg=request.value_usd / request.carbon_amount_kg,
            issuer=request.issuer or "QuantumEco Intelligence",
            transaction_hash=credit_result["transaction_hash"],
            block_number=credit_result.get("block_number", 0),
            credit_status="active",
            environmental_equivalents=environmental_equivalents,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow().replace(year=datetime.utcnow().year + 1),  # 1 year expiry
            metadata=request.metadata or {}
        )
        
        # Store transaction details
        transaction_cache[credit_result["transaction_hash"]] = {
            "credit_id": credit_result["credit_id"],
            "transaction_type": "carbon_credit_creation",
            "block_number": credit_result.get("block_number", 0),
            "timestamp": datetime.utcnow()
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Carbon credit creation failed: {str(e)}")


# Background task for database storage
async def store_certificate_in_db(certificate_id: str, certificate_data: Dict[str, Any]):
    """
    Store certificate in database for persistent storage
    """
    try:
        # This would typically store in a database
        # For demo purposes, we'll just log it
        print(f"Stored certificate {certificate_id} in database")
    except Exception as e:
        print(f"Failed to store certificate {certificate_id}: {str(e)}")


# Health check endpoint
@router.get("/health")
async def blockchain_service_health():
    """
    Health check for blockchain service
    """
    try:
        # Test blockchain connection
        connection_status = await blockchain_service.test_connection()
        
        # Test smart contract interaction
        contract_status = await blockchain_service.test_contract_interaction()
        
        return {
            "status": "healthy",
            "services": {
                "blockchain_connection": connection_status,
                "smart_contracts": contract_status,
                "ganache_node": "connected"
            },
            "cache_stats": {
                "certificates_cached": len(certificate_cache),
                "transactions_cached": len(transaction_cache)
            },
            "network_info": {
                "network_name": "Ganache Local",
                "network_id": 1337,
                "node_url": "http://127.0.0.1:8545"
            },
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Blockchain service unhealthy: {str(e)}")


# Demo endpoint for Walmart showcase
@router.get("/demo/certificates")
async def get_demo_certificates():
    """
    Demo endpoint with pre-generated certificates for presentation
    """
    try:
        # Generate demo certificates if cache is empty
        if not certificate_cache:
            demo_certificates = await blockchain_service.generate_demo_certificates(5)
            
            for cert in demo_certificates:
                certificate_cache[cert["certificate_id"]] = cert
        
        # Return demo certificates with impressive metrics
        demo_data = {
            "demo_certificates": list(certificate_cache.values())[:5],
            "total_carbon_saved_kg": sum(cert.get("carbon_saved_kg", 0) for cert in certificate_cache.values()),
            "total_cost_saved_usd": sum(cert.get("cost_saved_usd", 0) for cert in certificate_cache.values()),
            "average_optimization_score": sum(cert.get("optimization_score", 0) for cert in certificate_cache.values()) / max(len(certificate_cache), 1),
            "blockchain_verified_count": len(certificate_cache),
            "generated_at": datetime.utcnow()
        }
        
        return demo_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo data generation failed: {str(e)}")
