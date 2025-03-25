import json
import subprocess
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda function that runs a DDoS simulation using Ddosify Engine.
    The target URL is retrieved from environment variables.
    """
    try:
        # Get parameters from environment variables
        target = os.environ.get('TARGET_URL', 'https://example.com')
        duration = int(os.environ.get('DURATION_SECONDS', '10'))
        requests_per_second = int(os.environ.get('REQUESTS_PER_SECOND', '10'))
        
        # Log the attack parameters
        logger.info(f"Starting DDoS simulation against {target}")
        logger.info(f"Duration: {duration}s, RPS: {requests_per_second}")
        
        # Construct the ddosify command
        cmd = [
            "ddosify_engine",
            "-t", target,
            "-d", str(duration),
            "-n", str(requests_per_second),
            "-m", "GET"
        ]
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # Log the output
        logger.info(f"Command output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Command errors: {result.stderr}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'DDoS simulation completed',
                'target': target,
                'duration': duration,
                'requests_per_second': requests_per_second,
                'output': result.stdout,
                'errors': result.stderr
            })
        }
    
    except Exception as e:
        logger.error(f"Error executing DDoS simulation: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error executing DDoS simulation',
                'error': str(e)
            })
        }