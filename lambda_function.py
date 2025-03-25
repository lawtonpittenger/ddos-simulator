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
        target = os.environ['TARGET_URL']
        duration = int(os.environ['DURATION_SECONDS'])
        requests_per_second = int(os.environ['REQUESTS_PER_SECOND'])
        user_agent = 'DemoAttack'
        load_type = 'waved'
        
        # Calculate total number of requests
        total_requests = requests_per_second * duration
        
        # Log the attack parameters
        logger.info(f"Starting DDoS simulation against {target}")
        logger.info(f"Duration: {duration}s, RPS: {requests_per_second}, Total requests: {total_requests}")
        logger.info(f"User-Agent: {user_agent}, Load type: {load_type}")
        
        # Construct the ddosify command to match the original CLI pattern
        cmd = [
            "ddosify_engine",
            "-n", str(total_requests),
            "-d", str(duration),
            "-h", f"User-Agent: {user_agent}",
            "-t", target,
            "-l", load_type
        ]
        
        # Execute the command
        logger.info(f"Executing command: {' '.join(cmd)}")
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
                'total_requests': total_requests,
                'user_agent': user_agent,
                'load_type': load_type,
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